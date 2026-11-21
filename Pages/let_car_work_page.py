from selenium.webdriver.common.by import By


class LetCarWorkPage:

    CITY = (By.ID, "city")
    MAKE = (By.NAME, "manufacture")
    MODEL = (By.NAME, "model")
    GEAR = (By.NAME, "gear")
    WD = (By.NAME, "wheelsDrive")
    DOORS = (By.NAME, "doors")
    GEAR_AUTO = "auto"
    GEAR_MANUAL = "manual"
    WD_FWD = "FWD"
    WD_RWD = "RWD"
    WD_AWD = "AWD"
    FUEL_PETROL = "petrol"
    FUEL_DIESEL = "diesel"
    FUEL_HYBRID = "hybrid"
    FUEL_ELECTRIC = "electric"