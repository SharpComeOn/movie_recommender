import pandas as pd
class Recommendater:
    def __init__(self, user_id, method):
        self.user_id = user_id
        self.method = method

    def method1(self):
        data = {
            "user id": [420, 380, 390],
            "movie title": ['the godfather', 'Forrest Gump', 'The Dark Knight'],
            "genres": ['11', '22', '33']
        }

        return(pd.DataFrame(data))