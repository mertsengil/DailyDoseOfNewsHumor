import mysql.connector

class DBReader:
    #DB CONNECTION
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db_connection.cursor()

    #fetch all titles
    def fetch_all_titles(self):
        self.cursor.execute("SELECT title FROM news")
        titles = [title[0] for title in self.cursor.fetchall()]
        return titles

    # fetch content by title
    def fetch_content_by_title(self, title):
        query = "SELECT title, content, url FROM news WHERE title = %s"
        self.cursor.execute(query, (title,))
        result = self.cursor.fetchone()
        if result:
            return {'title': result[0], 'content': result[1], 'url': result[2]}
        else:
            return {'title': title, 'content': "Bu başlıkla ilgili içerik bulunamadı.", 'url': None}
    #CLOSE CONNECTION
    def close(self):
        self.cursor.close()
        self.db_connection.close()
