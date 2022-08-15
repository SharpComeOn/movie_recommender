import pandas as pd
class Recommendater:
    def __init__(self, user_id, method):
        self.user_id = user_id
        self.method = method

    def method1(self, user_id):
        data = {
            "user id": [420, 380, 390],
            "movie title": ['The godfather', 'Forrest Gump', 'The Dark Knight'],
            "genres": [user_id + '11', user_id + '22', user_id + '33']
        }
        return(pd.DataFrame(data))

    def method2(self, user_id):
        data = {
            "user id": [123, 234, 345],
            "movie title": ['Inception', 'Toy Story', 'Gone With the Wind'],
            "genres": [user_id + '11', user_id + '22', user_id + '33']
        }
        return(pd.DataFrame(data))