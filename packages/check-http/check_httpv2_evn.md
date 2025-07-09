# check_httpv2_evn - Erweiterte Inhaltsprüfung

## Beschreibung

Dieses Monitoring-Paket (MKP) enthält eine angepasste Version des `check_httpv2`-Plugins mit dem Namen `check_httpv2_evn`. Die Anpassung ermöglicht es, im Fehlerfall spezifische Teile aus dem Body einer HTTP-Antwort zu extrahieren und als Service-Zusammenfassung (Summary) in Checkmk anzuzeigen. Dies ist besonders nützlich für die Überwachung von APIs, die detaillierte Fehlermeldungen im JSON-Format zurückgeben.

## Funktionsweise

Die Kernfunktionalität basiert auf einer intelligenten Nutzung der Regex-Optionen des Checks:

1.  **Invertierte Regex-Prüfung:** Anstatt auf einen "OK"-Zustand zu prüfen, wird ein regulärer Ausdruck konfiguriert, der den **Fehlerfall** beschreibt.
2.  **Fehlerfall-Erkennung:** Die Option `--body-regex-invert` wird verwendet. Das bedeutet:
    *   **OK-Zustand:** Der Regex für den Fehlerfall findet **keine** Übereinstimmung im Antwort-Body. Durch die Invertierung ist der Check-Status **OK**.
    *   **Fehler-Zustand:** Der Regex findet eine Übereinstimmung. Der Check geht in den Zustand **WARNING**.
3.  **Dynamische Ausgabe:** Im Fehlerfall wird der gesamte Text, der vom regulären Ausdruck gefunden wurde, als Service-Output verwendet. Die Standard-Fehlermeldung wird dadurch ersetzt.

## Konfiguration

Die Konfiguration erfolgt über das Regelwerk **"Setup > Services > Other services > Integrate Nagios plug-ins"**.

**Kommandozeilen-Beispiel:**

```
check_httpv2_evn --url '$URL$' --method GET --body-regex '(?s)"msg":".*?".*"status":"-.*?".*"summary":\{.*\}' --body-regex-invert
```

*Anmerkung: Weitere Parameter wie Authentifizierung (`--auth-user`, etc.) können bei Bedarf hinzugefügt werden.*

### Wichtige Parameter erklärt

*   `--body-regex '(?s)"msg":".*?".*"status":"-.*?".*"summary":\{.*\}`'
    *   Dieser reguläre Ausdruck ist das Herzstück. Er ist so gestaltet, dass er nur zutrifft, wenn ein negativer Status (z.B. `"status":"-1"`) im JSON vorkommt.
    *   `(?s)`: Sorgt dafür, dass der Punkt `.` auch Zeilenumbrüche umfasst.
    *   `\{` und `\}`: Die geschweiften Klammern des `summary`-Objekts müssen mit einem Backslash maskiert werden, da sie in Regex eine Sonderbedeutung haben.
    *   Der Ausdruck ist so geschrieben, dass er die komplette relevante Zeile findet.

*   `--body-regex-invert`
    *   Dieser Schalter ist entscheidend. Er kehrt die Logik um und sorgt dafür, dass der Check nur dann fehlschlägt, wenn der Regex eine Übereinstimmung findet.

## Anwendungsbeispiel

Angenommen, eine API unter `https://sub.dom.tld/api/tool/spoolMonitor` wird überwacht.

**Antwort im OK-Fall:**
```json
{"msg":"ok","status":"1","summary":{"spoolsMissing":0,"spoolsTotal":42}}
```
Der Regex (`..."status":"-.*?"...`) findet keine Übereinstimmung. Wegen `--body-regex-invert` ist der Service-Status **OK**.

**Antwort im Fehlerfall:**
```json
{"msg":"spool error","status":"-1","summary":{"spoolsMissing":2,"spoolsTotal":42}}
```
Der Regex findet eine Übereinstimmung. Der Service-Status wird **WARNING**.

**Resultierender Service-Output in Checkmk:**
```
{"msg":"spool error","status":"-1","summary":{"spoolsMissing":2,"spoolsTotal":42}} (!)
```

Diese Konfiguration ermöglicht eine sehr präzise und informative Überwachung von API-Endpunkten.