# Create a Windows EXE with CompanyName = "SpectorOps" for MDE Testing

## 1. Install .NET SDK

Open PowerShell as Administrator:

```powershell
winget install Microsoft.DotNet.SDK.8
```

Verify:

```powershell
dotnet --version
```

---

## 2. Create a New Console Application

```powershell
mkdir C:\Temp\MDETest
cd C:\Temp\MDETest

dotnet new console -n MDETest
cd MDETest
```

---

## 3. Update Project Metadata

Replace the contents of `MDETest.csproj` with:

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>

    <AssemblyName>MDETest</AssemblyName>
    <Company>SpectorOps</Company>
    <Product>MDE Detection Test</Product>
    <Version>1.0.0</Version>
  </PropertyGroup>

</Project>
```

---

## 4. Replace Program.cs

```csharp
Console.WriteLine("MDE Detection Test");
```

---

## 5. Build the EXE

```powershell
dotnet publish -c Release -r win-x64 --self-contained true
```

The executable will be created at:

```text
bin\Release\net8.0\win-x64\publish\MDETest.exe
```

---

## 6. Verify CompanyName Metadata

```powershell
(Get-Item .\bin\Release\net8.0\win-x64\publish\MDETest.exe).VersionInfo.CompanyName
```

Expected output:

```text
SpectorOps
```

---

## 7. Execute the Binary

```powershell
.\bin\Release\net8.0\win-x64\publish\MDETest.exe
```

---

## 8. Verify in Microsoft Defender for Endpoint

```kusto
DeviceProcessEvents
| where FileName == "MDETest.exe"
| project Timestamp,
          DeviceName,
          FileName,
          ProcessVersionInfoCompanyName,
          InitiatingProcessVersionInfoCompanyName
| order by Timestamp desc
```

Expected:

```text
ProcessVersionInfoCompanyName = SpectorOps
```

or

```text
InitiatingProcessVersionInfoCompanyName = SpectorOps
```

This should trigger detections that match:

```kusto
InitiatingProcessVersionInfoCompanyName contains "SpectorOps"
```
