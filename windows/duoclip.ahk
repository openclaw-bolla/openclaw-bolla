; Bolla — Duo-Screenshot Hotkey (AutoHotkey v2)
; Win+Strg+S  ->  rechte Duo-Seite in die Windows-Zwischenablage
; Referenzkopie. Aktiv liegt die Datei unter %LOCALAPPDATA%\Bolla\ (vom Installer geschrieben).
#SingleInstance Force
A_IconTip := "Bolla: Win+Strg+S = Duo-Screenshot (rechte Seite) -> Zwischenablage"

#^s:: {
    Run('wscript.exe "' . A_AppData . '\..\Local\Bolla\duoclip_launch.vbs"', , "Hide")
}
