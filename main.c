/*
 * SpectorOps-branded MDE detection-test binary.
 *
 * Purpose: purely to exercise a custom MDE detection rule of the form
 *     InitiatingProcessVersionInfoCompanyName contains 'SpectorOps'
 *
 * This binary has NO offensive functionality. It only:
 *   1) prints status to stdout,
 *   2) spawns one benign child process (cmd.exe /c echo ...), and
 *   3) writes one small text file into %TEMP%.
 *
 * Both actions exist purely so MDE logs a telemetry event (process
 * creation / file creation) with THIS binary as the InitiatingProcess,
 * which is what populates InitiatingProcessVersionInfoCompanyName from
 * the CompanyName field embedded in this file's VERSIONINFO resource
 * (see version.rc). Safe to delete any artifacts it leaves behind.
 */

#include <windows.h>
#include <stdio.h>

int main(void) {
    printf("[*] SpectorOps detection-test binary starting (benign, no offensive functionality)\n");

    /* 1) Spawn a benign child process -> DeviceProcessEvents row with
          InitiatingProcessVersionInfoCompanyName = "SpectorOps". */
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    char cmdline[] = "cmd.exe /c echo SpectorOps-detection-test";

    if (CreateProcess(NULL, cmdline, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        printf("[*] Spawned child process, PID %lu\n", (unsigned long)pi.dwProcessId);
        WaitForSingleObject(pi.hProcess, 5000);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    } else {
        printf("[!] CreateProcess failed, GetLastError=%lu\n", (unsigned long)GetLastError());
    }

    /* 2) Write a small benign file -> DeviceFileEvents row with
          InitiatingProcessVersionInfoCompanyName = "SpectorOps". */
    char *tmp = getenv("TEMP");
    if (tmp) {
        char path[MAX_PATH];
        snprintf(path, sizeof(path), "%s\\spectorops_detection_test.txt", tmp);
        FILE *f = fopen(path, "w");
        if (f) {
            fprintf(f, "SpectorOps MDE detection-test artifact. Safe to delete.\n");
            fclose(f);
            printf("[*] Wrote test file: %s\n", path);
        }
    }

    printf("[*] Done.\n");
    return 0;
}
