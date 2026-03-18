import mysql.connector
# from outside uic, use pepchem.org instead of 10.124.181.40

cnx = mysql.connector.connect(host="10.124.181.40", user="job_scheduler", passwd="Illinois2018@)!*", port=35306)

cursor = cnx.cursor()

sql_query="""SELECT * from job_queue.parameters WHERE creator="ygao"; """

cursor.execute(sql_query)
results=cursor.fetchall()
results_list=[i for i in results]
for each in results_list:
    print(each)

sql_insert_query = 'INSERT INTO job_queue.parameters(creator, species, enzyme_specificity, max_missed_cleavage) VALUES ("ygao","mouse","1","1")'
cursor.execute(sql_insert_query)
cnx.commit()
cnx.close()