import subprocess
import os

SCRIPTS_DIR = r"C:\Users\Ritika Sharma\OneDrive - JK LAKSHMIPAT UNIVERSITY\Major_project\NJDG-Data-Extration-and-Analysis\rajasthan_scripts"

scripts = [
    "Ajmer.py",
    "Alwar.py",
    "Balotra_Barmer.py",
    "Banswara.py",
    "Baran.py",
    "Bharatpur.py",
    "Bhilwara.py",
    "Bikaner.py",
    "Bundi.py",
    "Chittorgarh.py",
    "Churu.py",
    "Dausa.py",
    "Dholpur.py",
    "Dungarpur.py",
    "Ganganagar.py",
    "Hanumangarh.py",
    "Jaipur_District.py",
    "Jaipur_Metro_I.py",
    "Jaipur_Metro_II.py",
    "Jaisalmer.py",
    "Jalore.py",
    "Jhalawar.py",
    "Jhunjhunu.py",
    "Jodhpur_District.py",
    "Jodhpur_Metro.py",
    "Karauli.py",
    "Kota.py",
    "Merta_Nagaur.py",
    "Pali.py",
    "Pratapgarh.py",
    "Rajsamand.py",
    "Sawai_Madhopur.py",
    "Sikar.py",
    "Sirohi.py",
    "Tonk.py",
    "Udaipur.py"
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
