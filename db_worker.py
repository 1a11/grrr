import sqlite3


class database():
    def __init__(self,  dbname):
        try:
            global conn
            conn = sqlite3.connect(dbname)
            global cursor
            cursor = conn.cursor()
        except Exception as exc:
            raise Exception(exc)
    #--<
    """
        If your database was f***ed up by something,  you can create new one

        create() - will create a new tables in your database
    """
    def create(self):
        cursor.execute("""CREATE TABLE settings
                  (channel text,  emoji text,  copypasta text, 
                   troll text,  insult text,  alt text)
               """)
        cursor.execute("""CREATE TABLE coefs
                  (channel text,  insult real,  troll real)
               """)
        
    #--<
    """
        Get colum values
        
        get_settings(channel) - will get values from table settings where channel is channel name
            channel - type: string,  example: '#abcdef'

        get_coefs(channel) - will get values from table coefs where channel is channel name
            channel - type: string,  example: '#abcdef'
    """       
    def get_settings(self,  channel):
        sql = "SELECT * FROM settings WHERE channel=?"
        cursor.execute(sql,  [(channel)])
        return cursor.fetchall()
    
    def get_coefs(self,  channel):
        sql = "SELECT * FROM coefs WHERE channel=?"
        cursor.execute(sql,  [(channel)])
        return cursor.fetchall()
    
    #--<
    """
        Creating colums for values
        
        create_settings(channel,  values) - will create new settings colum in table settings
            channel - type: string,  example: '#abcdef'
            values - type: dict,  example: {'emoji':'y', 'copypasta':'y', 'troll':'y', 'insult':'y', 'alt':'y'}

        create_coefs(channel,  values) - will create new coefs colum in table coefs
            channel - type: string,  example: '#abcdef'
            values - type: dict,  example: {'troll':0.96, 'insult':0.47}
    """
    
    def create_settings(self,  channel,  values):
        sql = """
        INSERT INTO settings
        VALUES ('{}', '{}', '{}', 
                '{}', '{}', '{}')
        """.format(channel, values['emoji'], values['copypasta'], 
                   values['troll'], values['insult'], values['alt'])
        print(sql)
        cursor.execute(sql)
        conn.commit()
        
    def create_coefs(self,  channel,  values):
        sql = """
        INSERT INTO coefs
        VALUES ('{}', '{}', '{}')
        """.format(channel,  values['troll'],  values['insult'])
        print(sql)
        cursor.execute(sql)
        conn.commit()

    #--<
    """
        Updating colums values
        
        set_settings(channel,  values) - will update values in table settings where channel is channel name and values are y/n (yes/no)
            channel - type: string,  example: '#abcdef'
            values - type: dict,  example: {'emoji':'y', 'copypasta':'y', 'troll':'y', 'insult':'y', 'alt':'y'}

        set_coefs(channel_values) - will update values in table coefs where channel is channel name and values are nn coefs
            channel - type: string,  example: '#abcdef'
            values - type: dict,  example: {'emoji':0.3, 'copypasta':0.50, 'troll':0.96, 'insult':0.47, 'alt':0.35}
    """    
    def set_settings(self,  channel,  values):
        sql = """
        UPDATE settings
        SET emoji = '{}', 
            copypasta = '{}', 
            troll = '{}', 
            insult = '{}', 
            alt = '{}'
        WHERE channel = '{}'
        """.format(values['emoji'], values['copypasta'], 
                   values['troll'], values['insult'], values['alt'],  channel)
        cursor.execute(sql)
        conn.commit()
        
    def set_coefs(self,  channel,  values):
        sql = """
        UPDATE settings
        SET troll = '{}', 
            insult = '{}'
        WHERE channel = '{}'
        """.format(values['troll'], values['insult'],  channel)
        cursor.execute(sql)
        conn.commit()
