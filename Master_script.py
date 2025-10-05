import subprocess
import os

SCRIPTS_DIR = r"C:\Users\Ritika Sharma\OneDrive - JK LAKSHMIPAT UNIVERSITY\Major_project\NJDG-Data-Extration-and-Analysis\data_collection_scripts"

scripts = [
    "Andaman_and_Nicobar.py",
    "Andhra_pradesh.py",
    "Arunachal_Pradesh.py",
    "Assam.py",
    "Bihar.py",
    "Chandigarh.py",
    "Chhattisgarh.py",
    "Delhi.py",
    "Goa.py",
    "Gujarat.py",
    "Haryana.py",
    "Himachal_Pradesh.py",
    "Jammu_and_Kashmir.py",
    "Jharkhand.py",
    "Karnataka.py",
    "Kerala.py",
    "Ladakh.py",
    "Lakshadweep.py",
    "Madhya_Pradesh.py",
    "Maharashtra.py",
    "Manipur.py",
    "Meghalaya.py",
    "Mizoram.py",
    "Nagaland.py",
    "Odisha.py",
    "Puducherry.py",
    "Punjab.py",
    "Rajasthan.py",
    "Sikkim.py",
    "Tamil_Nadu.py",
    "Telangana.py",
    "The_Dadra_and_Nagar_Haveli.py",
    "Tripura.py",
    "Uttar_Pradesh.py",
    "Uttrakhand.py",
    "West_Bengal.py"
]

for script in scripts:
    script_path = os.path.join(SCRIPTS_DIR, script)
    print(f"\n🚀 Running {script} ...")
    try:
        # result = subprocess.run(["python", script_path], capture_output=True, text=True)
        result = subprocess.run(["python", script_path])
        print(f"✅ Finished {script}")
        if result.stdout:
            print("Output:", result.stdout)
        if result.stderr:
            print("⚠️ Errors:", result.stderr)
    except Exception as e:
        print(f"❌ Could not run {script}: {e}")
