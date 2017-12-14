from twitterHandler import Twitter_User
import pandas as pd
import threading




if __name__=='__main__':
    usersIDS = {'User1':0000001,'User2':00000002,
                'User3':000003,'User4':0000004}
    threads = {}
    excel_writer = pd.ExcelWriter("Y-C Influencer Report.xlsx", engine='openpyxl')
    
    def get_data(user_id): #get best last tweets and store them in a excel file
        user = Twitter_User.Twitter_User(user_id,2000)
        user.get_tweets()
        #print(user.get_tweets())
        best_tweets = user.most_liked_rt()
        #print(best_tweets)
        best_tweets.to_excel(excel_writer, '{}'.format(user.name),index=False)
        excel_writer.save()
        excel_writer.close()
        
    
    for user_name,user_id in usersIDS.items():
        try:
            t = threading.Thread(target=get_data,args=(user_id,))
            threads[user_name] = t
            print('Starting to get data for: {}'.format(user_name))
            t.start()
        except Exception as e:
            print('Something wrong happens: ',e)


    for name,t in threads.items():
        t.join()
        print('Process for {} Stopped'.format(name))
   








