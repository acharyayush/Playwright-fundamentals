from robocorp.tasks import task
from RPA.Browser.Playwright import Playwright
from Browser.utils.data_types import SelectAttribute, SelectionStrategy, DialogAction, ElementState
from time import sleep
from utils import get_order_state, set_order_state
from RPA.Tables import Tables
from pathlib import Path
URL = "https://qa-practice.razvanvancea.ro"
CSV_BASE_PATH = "output/csv"
browser = Playwright()
FILE_PATH = "order_state.txt"
table_lib = Tables()
@task
def solve_challenge():
    
    browser.new_browser(headless=False, slowMo=0)
    
    try:
        #Create csv directory if it doesn't exist
        dir_path = Path("output/csv")
        dir_path.mkdir(parents=True, exist_ok=True)

        browser.new_page(URL)
        step_len = len(STEP_LIST)
        state = get_order_state(FILE_PATH)%step_len
        for i in range(state, step_len):
            STEP_LIST[i]()
            set_order_state(FILE_PATH, i+1)
        sleep(2)
    finally:
        logout()
        sleep(2)
        browser.close_browser()

def fill_register_form():
    """Fill up the register form and submit"""
    browser.go_to(URL + "/register.html")
    browser.type_text("#firstName", "Ayush")
    browser.type_text("#lastName", "Acharya")
    browser.type_text("#phone", "9864777435")
    browser.select_options_by("#countries_dropdown_menu", SelectAttribute.value ,"Nepal")
    browser.type_text("#emailAddress", "ayushacharya.htd057@gmail.com")
    browser.type_secret("#password", "password")
    browser.check_checkbox("#exampleCheck1")
    browser.click("#registerBtn")

def fill_login_form():
    """Fill up the login form and submit"""
    email = "admin@admin.com"
    password = "admin123"
    browser.go_to(URL+"/auth_ecommerce.html")
    browser.type_text("#email", email)
    browser.type_secret("#password", password)
    browser.click("#submitLoginBtn")

def logout():
    print(browser.get_element_count("a#logout"))
    if browser.get_element_count("a#logout")>0:
        browser.click("a#logout")

def recover_password():
    """Fill email and submit recover password button"""
    browser.go_to(URL+"/recover-password.html")
    email = "admin@admin.com"
    browser.type_text("input[type=email]", email)
    browser.click(".btn-primary")

def check_checkboxes():
    """Check all 3 checkboxes and uncheck 2nd one"""
    browser.go_to(URL+"/checkboxes.html")
    checkboxes = browser.get_elements("input[type=checkbox]")
    for checkbox in checkboxes:
        browser.check_checkbox(checkbox)
    sleep(1)
    browser.uncheck_checkbox(checkboxes[1])

def check_radiobuttons():
    """Check 2nd radio buttons and enable the last one"""
    browser.go_to(URL+"/radiobuttons.html")
    radio = browser.get_element("input[type=radio] >> nth=1")
    browser.check_checkbox(radio)
    browser.evaluate_javascript("input[type=radio] >> nth=3", "(el)=>el.removeAttribute('disabled')")

def window_section():
    """Click new tab button, close newly opened tab 
       navigate to window.html, click new window button and close the window"""
    browser.go_to(URL+"/tab.html")
    browser.click("#newTabBtn")
    browser.switch_page("NEW")
    browser.close_page()
    sleep(1)
    browser.go_to(URL+"/window.html")
    browser.click("#newWindowBtn")
    prev_page_id = browser.switch_page("NEW")
    browser.close_page()
    browser.switch_page(prev_page_id)
    sleep(1)

def double_click():
    browser.go_to(URL+"/double-click.html")
    browser.click_with_options("#double-click-btn", clickCount=2)

def scroll_to_bottom():
    """Scroll to the end of page where The End text is visible"""
    browser.go_to(URL+"/scroll.html")
    browser.scroll_to_element("#the-end")

def hover_button():
    """Hover to the button"""
    browser.go_to(URL+"/mouse-hover.html")
    browser.hover("#button-hover-over")

def toggle_text_display():
    """Change display to none, and then block again"""
    browser.go_to(URL+"/show-hide-element.html")
    browser.evaluate_javascript("#hiddenText", "el=>el.style.setProperty('display', 'none')")
    sleep(1)
    browser.go_to(URL+"/show-hide-element.html")
    browser.evaluate_javascript("#hiddenText", "el=>el.style.setProperty('display', 'block')")    

def extract_static_html_table_to_csv():
    """extract #peopleTable, convert it to csv and store inside output/csv directory"""
    browser.go_to(URL+"/web-table.html")
    #extract first row as header, others as data
    column = []
    for i in range(1,5):
        txt = browser.get_text(f"#peopleTable thead tr th:nth-child({i})")
        column.append(txt)
    table_data = [column]
    for j in range(1,6):
        new_row = []
        first_col_data = browser.get_text(f"#peopleTable tbody tr:nth-child({j}) th")
        new_row.append(first_col_data)
        for k in range(2, 5):
            #extract kth row data from 2nd to last
            data = browser.get_text(f"#peopleTable tbody tr:nth-child({j}) td:nth-child({k})")
            new_row.append(data)
        table_data.append(new_row)
    table_lib.write_table_to_csv(table=table_lib.create_table(table_data), header=False, path=f"{CSV_BASE_PATH}/static_table.csv")
        
def extract_dynamic_html_table_to_csv():
    """extract #peopleTable, convert it to csv and store inside output/csv directory"""
    browser.go_to(URL+"/dynamic-table.html")
    #extract first row as header, others as data
    column = []
    header_selectors = browser.get_elements(f"#data-table thead tr th")
    for header_selector in header_selectors:
        column.append(browser.get_text(header_selector))
    table_data = [column]
    row_length = len(browser.get_elements(f"#data-table tbody tr"))
    for j in range(1, row_length+1):
        new_row = []
        img_src = browser.get_attribute(f"#data-table tbody tr:nth-child({j}) td:nth-child(1) img", "src")
        new_row.append(img_src)
        for i in range(2, len(column)+1):
            data = browser.get_text(f"#data-table tbody tr:nth-child({j}) td:nth-child({i})")
            new_row.append(data)
        table_data.append(new_row)
    table_lib.write_table_to_csv(table=table_lib.create_table(table_data), header=False, path=f"{CSV_BASE_PATH}/dynamic_table.csv")

def select_dropdown():
    """Select country Nepal in single dropdown
        Select 4th level -2 in multi level dropdown"""
    browser.go_to(URL+"/dropdowns.html")
    browser.select_options_by("#dropdown-menu", SelectAttribute.value ,"Nepal")
    browser.click("#multi-level-dropdown-btn")
    dropdown_levels = browser.get_elements("ul li a.dropdown-item")
    for dropdown_level in dropdown_levels:
        browser.hover(dropdown_level)
    browser.click(browser.get_element_by(selection_strategy=SelectionStrategy.Text, text="4th level - 2"))

def iframe():
    """Click learn more button in iframe"""
    browser.go_to(URL+"/iframe.html")
    browser.click("iframe >>> #learn-more")

#TODO: NEED TO CANCEL CONFIRM DIALOG BUT COULD NOT
def alert():
    """Click Ok to alert and cancel to Confirm dialog boxes"""
    browser.go_to(URL+"/alerts.html")
    browser.handle_future_dialogs(action=DialogAction.accept)
    browser.click("#alert-btn")
    browser.click("#confirm-btn")

def file_upload():
    """Upload a file with the file path and click submit"""
    browser.go_to(URL+"/file-upload.html")
    FILE_PATH = "/Users/aacs/Downloads/Level3_certificate.pdf"
    browser.upload_file_by_selector("#file_upload", FILE_PATH)
    browser.click(".custom-file button[type=submit]")

def pick_date():
    """Add range date and simple date in date picker"""
    browser.go_to(URL+"/calendar.html")
    browser.type_text("#range-date-calendar","04/01/2017 - 05/31/2017")
    browser.click(".applyBtn")
    browser.type_text("#calendar","11/21/2003")
    #This removes the selector menu from screen (clicking anywhere on screen removes it, let's click on div with class 'line')
    browser.click("#content .line")

def text_after_loading():
    """Wait for loading to disappear and print innerHTML of div with id=content"""
    browser.go_to(URL+"/loader.html")
    browser.wait_for_elements_state("#loader", ElementState.hidden)
    browser.evaluate_javascript(
    "#content",
    """(element) => {
        const newEl = document.createElement('h1');
        newEl.textContent = 'This text was appended after loader disappeared';
        element.appendChild(newEl);
    }"""
    )

def pagination():
    """Click on 1,2,3,4,Next one after another"""
    browser.go_to(URL+"/pagination.html")
    pages = browser.get_elements("a.page-link")
    for i in range(1, len(pages)):
        browser.click(pages[i])


def update_cart():
    """Add first two items of Page 1 to cart
    Go to page 3
    Add 3rd and 4th items to cart
    Make first items quantity as 3
    remove 2nd item from cart"""
    browser.click(".shop-item:nth-child(1) button")
    browser.click(".shop-item:nth-child(2) button")
    page3_selector = "#pagination-controls nav button:text-is('3')"
    browser.click(page3_selector)
    browser.click(".shop-item:nth-child(3) button")
    browser.click(".shop-item:nth-child(4) button")
    browser.type_text(".cart-items .cart-row:nth-child(1) .cart-quantity-input", "3")
    browser.click(".cart-items .cart-row:nth-child(2) .btn-danger")

def checkout():
    """Click proceed to checkout button
    Fill shipping details
    Click Submit order button
    """
    browser.click(".btn-purchase")
    browser.type_text("#phone", "9864777435")
    browser.type_text("input[name=street]", "Bindabasini")
    browser.type_text("input[name=city]", "Hetauda")
    browser.select_options_by("#countries_dropdown_menu", SelectAttribute.value, "Nepal")
    browser.click("#submitOrderBtn")

def shop_some_items():
    """Login first
       Update cart
       Proceed to checkout
        """
    fill_login_form()
    update_cart()
    checkout()
STEP_LIST = [fill_register_form, recover_password, check_checkboxes, check_radiobuttons, window_section, 
double_click, scroll_to_bottom, hover_button, toggle_text_display, extract_static_html_table_to_csv, extract_dynamic_html_table_to_csv, select_dropdown, iframe, alert, file_upload, pick_date, text_after_loading, pagination, shop_some_items]
