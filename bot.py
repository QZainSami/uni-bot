import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# ⚙️ CONFIGURATION - ENTER YOUR DETAILS HERE
# ==========================================
USERNAME = "YOUR_ENROLLMENT_HERE"  # e.g., "02-134242-015"
PASSWORD = "YOUR_PASSWORD_HERE"
INSTITUTE_VALUE = "2"              # 2 is for Karachi Campus

LOGIN_URL = "https://cms.bahria.edu.pk/Logins/Student/Login.aspx"
SURVEY_DASHBOARD_URL = "https://cms.bahria.edu.pk/Sys/Student/QualityAssurance/QualityAssuranceSurveys.aspx"

def automate_surveys():
    print("🚀 Starting the Bahria Survey Bot...")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        # --- 1. LOGIN ---
        print("Logging in...")
        driver.get(LOGIN_URL)
        
        wait.until(EC.presence_of_element_located((By.ID, "BodyPH_tbEnrollment"))).send_keys(USERNAME)
        driver.find_element(By.ID, "BodyPH_tbPassword").send_keys(PASSWORD)
        Select(driver.find_element(By.ID, "BodyPH_ddlInstituteID")).select_by_value(INSTITUTE_VALUE)
        driver.find_element(By.ID, "BodyPH_btnLogin").click()
        
        print("✅ Logged in successfully!")
        time.sleep(3) 

        # --- 2. GO TO SURVEY DASHBOARD ---
        print("Navigating to pending surveys...")
        driver.get(SURVEY_DASHBOARD_URL)
        
        table = wait.until(EC.presence_of_element_located((By.ID, "BodyPH_gvSurveyConducts")))
        evaluate_buttons = table.find_elements(By.LINK_TEXT, "Evaluate")
        
        survey_urls = [btn.get_attribute("href") for btn in evaluate_buttons]
        
        if not survey_urls:
            print("🎉 No pending surveys found! You are all caught up.")
            return

        print(f"🎯 Found {len(survey_urls)} surveys to complete.")

        # --- 3. LOOP THROUGH EACH SURVEY ---
        for index, url in enumerate(survey_urls):
            print(f"📝 Filling out survey {index + 1} of {len(survey_urls)}...")
            driver.get(url)
            time.sleep(2) 
            
            # --- THE SMART JAVASCRIPT ---
            js_script = """
            let questionNames = [...new Set(Array.from(document.querySelectorAll('input[type="radio"]')).map(r => r.name))];
            
            questionNames.forEach(name => {
                let options = document.querySelectorAll(`input[name="${name}"]`);
                
                if (options.length === 5) {
                    options[1].click(); // Clicks "Agree"
                } else if (options.length > 0) {
                    // Demographic Questions
                    let clicked = false;
                    
                    options.forEach(opt => {
                        let id = opt.id;
                        let label = document.querySelector(`label[for="${id}"]`);
                        let text = label ? label.innerText.toLowerCase() : opt.value.toLowerCase();
                        
                        // Selects Full Time, No (Disability), or Collaborative
                        if (text.includes("full time") || text.includes("no") || text.includes("collaborative")) {
                            opt.click();
                            clicked = true;
                        }
                    });
                    
                    // Fallback for Gender/Age (Clicks first option: Male / <22)
                    if (!clicked) {
                        options[0].click();
                    }
                }
            });
            """
            driver.execute_script(js_script)
            time.sleep(1) 
            
            # --- AGGRESSIVE SUBMIT BUTTON FINDER ---
            try:
                aggressive_selector = "[id*='Save'], [id*='Submit'], [id*='btnSave'], input[value='Save'], input[value='Submit'], input[type='submit']"
                
                buttons = driver.find_elements(By.CSS_SELECTOR, aggressive_selector)
                submit_clicked = False
                
                for btn in buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        submit_clicked = True
                        print(f"✅ Survey {index + 1} submitted successfully!")
                        break
                        
                if not submit_clicked:
                    print(f"⚠️ Could not find a visible submit button for survey {index + 1}. You may need to click it manually.")
                    
            except Exception as e:
                print(f"⚠️ Error clicking submit for survey {index + 1}: {e}")
            
            time.sleep(2) 

    except Exception as e:
        print(f"❌ A critical error occurred: {e}")
    finally:
        print("🏁 Bot finished looping through surveys.")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    automate_surveys()