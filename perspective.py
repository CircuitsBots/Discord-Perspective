import os

import flask
from googleapiclient import discovery
from dotenv import load_dotenv

load_dotenv()

webapp = flask.Flask(__name__)


class PerspectiveApi:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=self.api_key,
            discoveryServiceUrl=(
                "https://commentanalyzer.googleapis.com/"
                "$discovery/rest?version=v1alpha1"
            ),
            static_discovery=False,
        )

    def analize_comment(self, comment: str) -> int:
        data = {
            "comment": {"text": comment},
            "requestedAttributes": {"TOXICITY": {}},
        }
        return self.client.comments().analyze(body=data).execute()


@webapp.route("/analize")
def analize():
    comment = flask.request.args["comment"]
    toxicity = webapp.config["papi"].analize_comment(
        comment
    )["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return flask.jsonify(toxicity=toxicity)


if __name__ == "__main__":
    webapp.config["papi"] = PerspectiveApi()
    webapp.run("localhost", 5050)
