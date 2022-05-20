from controllers.base import Controller
from views.base import CommandView, ActorsReport, TournamentReport


def main():
    view = CommandView()
    actors_report = ActorsReport()
    tournament_report = TournamentReport()
    controller = Controller(view, actors_report, tournament_report)
    controller.run()


if __name__ == "__main__":
    main()
