from src.models.claan import Claan
from src.utils.claan_page import ClaanPage

from menu import menu_with_redirect


def main() -> None:
    ClaanPage(Claan.WAVE_RIDERS)


if __name__ == "__main__":
    main()
