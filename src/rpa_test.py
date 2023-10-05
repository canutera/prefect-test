from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import pyautogui
import pygetwindow, os
import pywinauto
from prefect import flow, task
from time import sleep

@task
def get_borders_list():
    driver = webdriver.Chrome()

    driver.get("https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_number_of_land_borders")
    print('getting table from wikipedia...')
    title = driver.title
    assert "List of countries and territories by number of land borders" in title

    driver.implicitly_wait(0.5)
    df = pd.read_html(driver.page_source)[0]
    driver.quit()

    return df


@task
def write_to_notepad(df:pd.DataFrame):
    print('opening notepad...')
    os.startfile(r"C:\WINDOWS\system32\notepad.exe")
    sleep(1)
    window = pyautogui.getWindowsWithTitle('Notepad')[-1]
    window.maximize()
    pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
    print('typing...')
    pyautogui.typewrite(df.head(3).to_string())
    sleep(8)
    
@task
def delete_if_exists(file:str=r"C:\Users\gabri\Documents\test.txt"):
    if os.path.isfile(file):
        os.remove(file)
        return 'File Deleted!' 
    return 'File did not exist...'

@task
def save_notepad():
    print('saving notepad file in documents folder...')
    window = pygetwindow.getWindowsWithTitle('Notepad')[-1]
    window.maximize()
    window.activate()
    pyautogui.moveTo(window.left +25,window.top +40)
    pyautogui.click()
    pyautogui.moveTo(window.left +25,window.top +125)
    pyautogui.click()
    pyautogui.typewrite('test.txt')
    sleep(3)
    pyautogui.press('enter') 
    sleep(3)
    window.close()
    sleep(1)

@flow(log_prints=True)
def main():
    df = get_borders_list()
    write_to_notepad(df)
    delete_if_exists()
    save_notepad()
    a = pd.read_fwf(rf"C:\Users\{os.getlogin()}\Documents\test.txt")
    print('shape:', a.shape)
    print('columns:', len(a.columns))


if __name__ == "__main__":
    main()