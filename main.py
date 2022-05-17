from controllers.base import Controller
from views.base import Command, Actors_report, Tournament_report


def main():
    view = Command()
    actors_report = Actors_report()
    tournament_report = Tournament_report()
    controller = Controller(view, actors_report, tournament_report)
    controller.run()


if __name__ == "__main__":
    main()
