from tkinter import *
from tkinter import ttk, messagebox, simpledialog

from connector.subscription_manager import SubscriptionManager


class TopicSelector():

    def __init__(self,topic_list):
        self.topic_list =topic_list

    def show_selector(self):
        ws  = Tk()
        ws.title('Topic List')
        ws.geometry('900x400')
        #ws['bg'] = '#AC99F2'

        game_frame = Frame(ws)

        self.my_game = ttk.Treeview(game_frame)

        self.my_game['columns'] = ('topic', 'message_type', 'monitoring_frequency')

        self.my_game.column("#0", width=0,  stretch=NO)
        self.my_game.column("topic",anchor=CENTER, width=250)
        self.my_game.column("message_type",anchor=CENTER,width=250)
        self.my_game.column("monitoring_frequency",anchor=CENTER,width=200)

        self.my_game.heading("#0",text="",anchor=CENTER)
        self.my_game.heading("topic",text="Topic",anchor=CENTER)
        self.my_game.heading("message_type",text="Message Type",anchor=CENTER)
        self.my_game.heading("monitoring_frequency",text="Monitoring Frequency",anchor=CENTER)

        for num,topic in enumerate(self.topic_list):
            #print(topic)
            topic.append(0)
            self.my_game.insert(parent='',index='end',iid=num,text='t', values=(topic[0],topic[1], topic[2]))



        #Entry boxes
        # playerid_entry= Entry(self.my_game)
        # playerid_entry.grid(row= 0, column=1)
        #
        # playername_entry = Entry(game_frame)
        # playername_entry.grid(row=1,column=1)
        #
        # playerrank_entry = Entry(game_frame)
        # playerrank_entry.grid(row=1,column=2)
        game_frame.pack()

        self.my_game.pack()
        self.my_game.bind('<Double-1>', self.subscribe)

        ws.mainloop()

    def subscribe(self,event):

        index = int(self.my_game.focus())
        selected_item= self.topic_list[index]
        topic = selected_item[0]
        sell  =self.my_game.selection()
        if not SubscriptionManager.is_subscribed(topic):
            val = simpledialog.askfloat("Monitoring Interval", "Select interval (s)")
            messagebox.showinfo(title='Subscribing', message=f'Subscribed to topic {topic} ')
            selected_item[2]=val
            SubscriptionManager.subscribe(topic,selected_item[1],val)
            self.my_game.delete(sell)
            self.my_game.insert(parent='', tag=index ,index=index,iid=index,text='t', values=(selected_item[0],selected_item[1], selected_item[2]))
            self.my_game.tag_configure(tagname=index, background='#A6F2A5')
        else:
            messagebox.showinfo(title='Unsubscribing', message=f'Unsubscribed from topic {topic}')
            SubscriptionManager.unsubscribe(topic)
            self.my_game.delete(sell)
            self.my_game.insert(parent='',index=index,iid=index,text='t', values=(selected_item[0],selected_item[1], 0))



if __name__ == '__main__':
    sel = TopicSelector([])

    sel.show_selector()
