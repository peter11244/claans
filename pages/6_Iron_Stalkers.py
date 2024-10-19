from src.models.claan import Claan
from src.utils.claan_page import ClaanPage


from menu import menu_with_redirect

def main() -> None:
    menu_with_redirect()
    ClaanPage(Claan.IRON_STALKERS)


if __name__ == "__main__":
    main()
