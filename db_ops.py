import json
import mysql.connector

#write the scraped data from the website to MySQL

class DBManager:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db_connection.cursor()

    def read_json_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def insert_data_into_db(self, data):
        insert_query = """
        INSERT INTO NEWS (title, content, url)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        content = VALUES(content), url = VALUES(url);
        """

        for article in data:
            try:
                self.cursor.execute(insert_query, (article['title'], article['content'], article['url']))
                self.db_connection.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print(f"Failed to insert/update data for title: {article['title']}")

    def close(self):
        self.cursor.close()
        self.db_connection.close()


