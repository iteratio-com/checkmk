//
//
// Support for the Zip and Cab Files
//
//

#include "stdafx.h"

#include "wnx/zip.h"

#include <fmt/format.h>
#include <fmt/xchar.h>
#include <shellapi.h>

#include <array>
#include <filesystem>
#include <fstream>

#include "common/cfg_info.h"
#include "common/wtools.h"
#include "tools/_process.h"
#include "wnx/logger.h"
namespace fs = std::filesystem;

template <typename R>
concept HasRelease = requires(R *r) {
    { r->Release() };
};

namespace cma::tools::zip {
// usually this pointer comes from Windows API
template <HasRelease R>
struct ResourceReleaser {
    void operator()(R *r) noexcept {
        if (r) r->Release();
    }
};

// usage
#if (0)
ReleasedResource<FolderItems> fi(::WindowsApiToGetFi());
#endif
//
template <HasRelease T>
using ReleasedResource = std::unique_ptr<T, ResourceReleaser<T>>;

static void InitVariant(VARIANT &var, BSTR bstr) {
    VariantInit(&var);
    var.vt = VT_BSTR;
    var.bstrVal = bstr;
}

static void InitVariantZipOptions(VARIANT &var) {
    VariantInit(&var);
    var.vt = VT_I4;
    var.lVal = FOF_NO_UI;
}

static void InitVariantFolderIetms(VARIANT &var, FolderItems *fi) {
    VariantInit(&var);
    var.vt = VT_DISPATCH;
    var.pdispVal = fi;
}

static HRESULT UnzipExec(Folder *to, FolderItems *fi) {
    VARIANT options = {};
    InitVariantZipOptions(options);

    VARIANT items = {};
    InitVariantFolderIetms(items, fi);

    return to->CopyHere(items, options);
}

static ReleasedResource<Folder> CreateFolder(IShellDispatch *dispatch,
                                             const wtools::Bstr &bstr) {
    VARIANT variant_dir = {};
    InitVariant(variant_dir, bstr.bstr());
    Folder *folder = nullptr;
    auto result = dispatch->NameSpace(variant_dir, &folder);

    if (!SUCCEEDED(result)) {
        XLOG::l("Error during NameSpace 1 /unzip/ {:#X}", result);
        return nullptr;
    }

    return ReleasedResource<Folder>{folder};
}

static bool CheckTheParameters(std::filesystem::path file,
                               std::filesystem::path dir) {
    if (!fs::exists(file) || !fs::is_regular_file(file)) {
        XLOG::l("File '{}' is absent or not suitable", file);
        return false;
    }

    if (!fs::exists(dir) || !fs::is_directory(dir)) {
        XLOG::l("Dir '{}' is absent or not suitable to unzip", dir);
        return false;
    }

    return true;
}

static ReleasedResource<IShellDispatch> CreateShellDispatch() {
    IShellDispatch *dispatch = nullptr;
    auto hres = CoCreateInstance(CLSID_Shell, nullptr, CLSCTX_INPROC_SERVER,
                                 IID_IShellDispatch,
                                 reinterpret_cast<void **>(&dispatch));
    if (!SUCCEEDED(hres)) {
        XLOG::l("Error during Create Instance /unzip/ {:X}", hres);
        return nullptr;
    }

    return ReleasedResource<IShellDispatch>{dispatch};
}

static ReleasedResource<FolderItems> GetFolderItems(Folder *folder) {
    FolderItems *fi = nullptr;
    folder->Items(&fi);
    return ReleasedResource<FolderItems>{fi};
}

namespace {

zip::Type GetFileType(std::wstring_view name) noexcept {
    constexpr std::array cab_header{'M', 'S'};
    constexpr std::array zip_header{'P', 'K'};
    try {
        std::ifstream f(wtools::ToUtf8(name), std::ios::binary);
        if (!f.good()) {
            return Type::unknown;
        }

        std::array<char, 2> header;
        f.read(header.data(), 2);
        if (header == cab_header) {
            return Type::cab;
        }
        if (header == zip_header) {
            return Type::zip;
        }
        XLOG::l("Header is not known '{}{}'", header[0], header[1]);
    } catch (const std::exception &e) {
        // catching possible exceptions in the
        // ifstream or memory allocations
        XLOG::l("Exception '{}' generated reading header", e.what());
    }
    return Type::unknown;
}

bool UnzipFile(std::wstring_view file_src, std::wstring_view dir_dest) {
    wtools::Bstr src(file_src);
    wtools::Bstr dest(dir_dest);

    wtools::InitWindowsCom();

    auto dispatch = CreateShellDispatch();
    if (nullptr == dispatch) {
        XLOG::l("Error during Create Instance /unzip/");
        return false;
    }

    auto to_folder = CreateFolder(dispatch.get(), dest);  // out
    if (to_folder == nullptr) {
        XLOG::l("Error finding folder /unzip/");
        return false;
    }

    auto from_file = CreateFolder(dispatch.get(), src);  // in
    if (from_file == nullptr) {
        XLOG::l("Error finding from file /unzip/. The file is '{}'",
                wtools::ToUtf8(file_src));
        return false;
    }

    // files & folders
    auto file_items = GetFolderItems(from_file.get());
    if (file_items == nullptr) {
        XLOG::l("Failed to get folder items /unzip/. The file is '{}'",
                wtools::ToUtf8(file_src));
        return false;
    }

    auto hres = UnzipExec(to_folder.get(), file_items.get());

    if (hres != S_OK) {
        XLOG::l("Error during copy here /unzip/ {:#X}", hres);
        return false;
    }

    XLOG::l.i("SUCCESS /unzip/");
    return true;
}

bool UncabFile(std::wstring_view file_src, std::wstring_view dir_dest) {
    auto command_line = fmt::format(L"expand {} -F:* {}", file_src, dir_dest);
    XLOG::l.i("Executing '{}'", wtools::ToUtf8(command_line));
    return RunCommandAndWait(command_line);
}
}  // namespace

bool Extract(const std::filesystem::path &file_src,
             const std::filesystem::path &dir_dest) {
    if (!CheckTheParameters(file_src, dir_dest)) {
        return false;
    }

    switch (GetFileType(file_src.wstring())) {
        case Type::zip:
            return UnzipFile(file_src.wstring(), dir_dest.wstring());
        case Type::cab:
            return UncabFile(file_src.wstring(), dir_dest.wstring());
        case Type::unknown:
            return false;
    }

    // unreachable
    return false;
}
}  // namespace cma::tools::zip
