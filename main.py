import sys
import sqlite3
import io
from smtplib import SMTP
from email.message import EmailMessage
from random import randint
from json import load, dump
from difflib import get_close_matches as gcm
from datetime import date, timedelta
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox,QLineEdit,QApplication,QDialog, QVBoxLayout, QScrollArea, QLabel, QGraphicsOpacityEffect,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt


# Connect to the database
conn = sqlite3.connect("library.db")
c = conn.cursor()

# Create tables if they don't exist 
c.execute(
    """CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                name TEXT,
                last_name TEXT,
                user_name TEXT,
                National_Code INTEGER,
                grade INTEGER,
                class INTEGER,
                email TEXT,
                rating TEXT,
                password TEXT
            )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS admin_user (
                id INTEGER PRIMARY KEY,
                name TEXT,
                last_name TEXT,
                user_name TEXT,
                National_Code INTEGER,
                email TEXT,
                rating TEXT,
                password TEXT
            )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                name TEXT,
                author TEXT,
                translator TEXT,
                publisher TEXT,
                publish_year INTEGER,
                inventory INTEGER,
                genre TEXT,
                pages INTEGER,
                inventory_unchangeable INTEGER,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS barrower (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                name_user TEXT,
                last_name TEXT,
                grade INTEGER,
                class INTEGER,
                email TEXT,
                name TEXT,
                author TEXT,
                translator TEXT,
                publisher TEXT,
                publish_year INTEGER,
                genre TEXT,
                pages INTEGER,
                giving_back TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )"""
)

with io.open("./GUI x Persian.ui", 'w', encoding='utf-8') as file:
    file.write('''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>603</width>
    <height>531</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>603</width>
    <height>531</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>603</width>
    <height>531</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>مدیریت کتابخانه</string>
  </property>
  <property name="windowIcon">
   <iconset>
    <normaloff>library.png</normaloff>library.png</iconset>
  </property>
  <property name="styleSheet">
   <string notr="true">font: 12pt &quot;Aviny&quot;;


</string>
  </property>
  <widget class="QPushButton" name="remove__book">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>210</x>
     <y>290</y>
     <width>151</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>پس گرفتن کتاب</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>giving.png</normaloff>giving.png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>30</width>
     <height>30</height>
    </size>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="show__book">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>190</x>
     <y>370</y>
     <width>191</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>نشان دادن کتاب ها</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>book.png</normaloff>book.png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>30</width>
     <height>30</height>
    </size>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="login">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>10</y>
     <width>101</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>ورود</string>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="exit">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>220</x>
     <y>490</y>
     <width>131</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="mouseTracking">
    <bool>false</bool>
   </property>
   <property name="inputMethodHints">
    <set>Qt::ImhNone</set>
   </property>
   <property name="text">
    <string>خروج</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>button.png</normaloff>button.png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>20</width>
     <height>20</height>
    </size>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="add__book">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>220</x>
     <y>250</y>
     <width>131</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>اضافه کردن کتاب</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>plus.png</normaloff>plus.png</iconset>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="list__of_borrowed_books">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>180</x>
     <y>410</y>
     <width>211</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>کتاب هایی که قرض گرفته شده</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>contact-list.png</normaloff>contact-list.png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>30</width>
     <height>30</height>
    </size>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="barrow__book">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>200</x>
     <y>330</y>
     <width>171</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>قرض گرفتن کتاب</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>delete.png</normaloff>delete.png</iconset>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="list__of_removed_books">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>150</x>
     <y>450</y>
     <width>281</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>کتاب هایی که پس داده شده است</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>lectern.png</normaloff>lectern.png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>30</width>
     <height>30</height>
    </size>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="sign__up">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>10</y>
     <width>101</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>ثبت نام</string>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="default">
    <bool>false</bool>
   </property>
   <property name="flat">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QComboBox" name="admin_combobox">
   <property name="enabled">
    <bool>false</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>550</y>
     <width>91</width>
     <height>41</height>
    </rect>
   </property>
   <property name="sizePolicy">
    <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
     <horstretch>0</horstretch>
     <verstretch>0</verstretch>
    </sizepolicy>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="iconSize">
    <size>
     <width>40</width>
     <height>40</height>
    </size>
   </property>
   <property name="frame">
    <bool>false</bool>
   </property>
   <item>
    <property name="text">
     <string/>
    </property>
    <property name="icon">
     <iconset>
      <normaloff>businessman.png</normaloff>businessman.png</iconset>
    </property>
   </item>
   <item>
    <property name="text">
     <string>درباره</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>خروج از اکانت</string>
    </property>
   </item>
  </widget>
  <widget class="QComboBox" name="normal_combobox">
   <property name="enabled">
    <bool>false</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>550</y>
     <width>91</width>
     <height>41</height>
    </rect>
   </property>
   <property name="sizePolicy">
    <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
     <horstretch>0</horstretch>
     <verstretch>0</verstretch>
    </sizepolicy>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="autoFillBackground">
    <bool>true</bool>
   </property>
   <property name="iconSize">
    <size>
     <width>40</width>
     <height>40</height>
    </size>
   </property>
   <property name="duplicatesEnabled">
    <bool>false</bool>
   </property>
   <property name="frame">
    <bool>false</bool>
   </property>
   <item>
    <property name="text">
     <string/>
    </property>
    <property name="icon">
     <iconset>
      <normaloff>student.png</normaloff>student.png</iconset>
    </property>
   </item>
   <item>
    <property name="text">
     <string>درباره</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>خروج از اکانت</string>
    </property>
   </item>
  </widget>
  <widget class="QPushButton" name="admin__maker">
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>10</y>
     <width>101</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>ثبت اکانت ادمین</string>
   </property>
  </widget>
  <widget class="QPushButton" name="changing__inventory_sum">
   <property name="enabled">
    <bool>false</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>200</x>
     <y>560</y>
     <width>151</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>افزایش تعداد اصلی کتاب</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>E:/kharazmi/project1/plus.png</normaloff>E:/kharazmi/project1/plus.png</iconset>
   </property>
  </widget>
  <widget class="QPushButton" name="changing__inventory_minus">
   <property name="enabled">
    <bool>false</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>370</x>
     <y>560</y>
     <width>151</width>
     <height>28</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>Aviny</family>
     <pointsize>12</pointsize>
     <weight>50</weight>
     <italic>false</italic>
     <bold>false</bold>
    </font>
   </property>
   <property name="text">
    <string>کاهش تعداد اصلی کتاب</string>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>E:/kharazmi/project1/delete.png</normaloff>E:/kharazmi/project1/delete.png</iconset>
   </property>
  </widget>
  <widget class="QPushButton" name="bot_support">
   <property name="geometry">
    <rect>
     <x>420</x>
     <y>0</y>
     <width>171</width>
     <height>101</height>
    </rect>
   </property>
   <property name="styleSheet">
    <string notr="true">image: url(:/technical-support.png);</string>
   </property>
   <property name="text">
    <string/>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>technical-support (1).png</normaloff>technical-support (1).png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>90</width>
     <height>90</height>
    </size>
   </property>
   <property name="shortcut">
    <string/>
   </property>
   <property name="autoDefault">
    <bool>true</bool>
   </property>
   <property name="flat">
    <bool>true</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="back">
   <property name="geometry">
    <rect>
     <x>-30</x>
     <y>0</y>
     <width>651</width>
     <height>831</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
   <property name="icon">
    <iconset>
     <normaloff>back.png</normaloff>back.png</iconset>
   </property>
   <property name="iconSize">
    <size>
     <width>700</width>
     <height>2000</height>
    </size>
   </property>
   <property name="flat">
    <bool>true</bool>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton_2">
   <property name="enabled">
    <bool>false</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>-10</x>
     <y>0</y>
     <width>601</width>
     <height>521</height>
    </rect>
   </property>
   <property name="maximumSize">
    <size>
     <width>16777215</width>
     <height>16777215</height>
    </size>
   </property>
   <property name="text">
    <string/>
   </property>
   <property name="flat">
    <bool>true</bool>
   </property>
  </widget>
  <zorder>back</zorder>
  <zorder>pushButton_2</zorder>
  <zorder>admin__maker</zorder>
  <zorder>sign__up</zorder>
  <zorder>remove__book</zorder>
  <zorder>show__book</zorder>
  <zorder>login</zorder>
  <zorder>exit</zorder>
  <zorder>add__book</zorder>
  <zorder>list__of_borrowed_books</zorder>
  <zorder>barrow__book</zorder>
  <zorder>list__of_removed_books</zorder>
  <zorder>normal_combobox</zorder>
  <zorder>admin_combobox</zorder>
  <zorder>changing__inventory_sum</zorder>
  <zorder>changing__inventory_minus</zorder>
  <zorder>bot_support</zorder>
 </widget>
 <resources>
  <include location="E:/images.qrc"/>
 </resources>
 <connections/>
</ui>''')

# GUI class
class Ui(QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        #showing ui file 
        
        
        uic.loadUi("./GUI x Persian.ui", self)
        self.show()


        QtGui.QFontDatabase.addApplicationFont('./Aviny.ttf')
        now = date.today()
        self.time_extend_email(now)


          
            # Connecting buttons
        self.add__book.clicked.connect(self.add_book)
        self.exit.clicked.connect(self.exitt)
        self.remove__book.clicked.connect(self.remove_book)
        self.show__book.clicked.connect(self.show_books)
        self.sign__up.clicked.connect(self.sign_up)
        self.login.clicked.connect(self.log_in)
        self.barrow__book.clicked.connect(self.borrow_book)
        self.list__of_borrowed_books.clicked.connect(self.list_of_borrowed_books)
        self.list__of_removed_books.clicked.connect(self.list_of_removed_books)
        self.admin__maker.clicked.connect(self.admin_maker)
        self.changing__inventory_sum.clicked.connect(self.changing_inventory_sum)
        self.changing__inventory_minus.clicked.connect(self.changing_inventory_minus)
        self.normal_combobox.activated.connect(self.combo_box_action) 
        self.admin_combobox.activated.connect(self.combo_box_action) 
        self.bot_support.clicked.connect(self.chat_bot)
             
            #variables for using buttons
        self.admin_combo = False
        self.normal_combo = False
        self.current_user_name = None
        self.current_user_last = None
        self.runner = False
        self.admin_maker_combo = None
        self.admin_access =False
        self.logged_in_user_id = None
        self.logged_in_user = None

            
            #applying opacity control on variables         
        opacity_effect_admin = QGraphicsOpacityEffect() 
        opacity_effect_normal = QGraphicsOpacityEffect() 
        opacity_effect_inventory_sum = QGraphicsOpacityEffect()
        opacity_effect_inventory_minus = QGraphicsOpacityEffect()
            #percent of opacity
        opacity_effect_admin.setOpacity(0) 
        opacity_effect_normal.setOpacity(0) 
        opacity_effect_inventory_sum.setOpacity(0)
        opacity_effect_inventory_minus.setOpacity(0)

            #seting opacity's  
        self.admin_combobox.setGraphicsEffect(opacity_effect_admin)
        self.normal_combobox.setGraphicsEffect(opacity_effect_normal)
        self.changing__inventory_sum.setGraphicsEffect(opacity_effect_inventory_sum)
        self.changing__inventory_minus.setGraphicsEffect(opacity_effect_inventory_minus)
  
    def load_json(self,path = str) -> dict:
        with open(f'./{path}', 'r+') as knowlege:
            data: dict =load(knowlege)
        return data
    def save_knowlege(self,path : str, data:dict):
        with open(f'./{path}', 'w+') as knowlege:
            dump(data, knowlege, indent=2)
    def best_matches(self,user_questions:str, question:list[str]) -> str | None:
        matches : list = gcm (user_questions,question,n=1,cutoff=0.4)
        return matches[0] if matches else None
    def get_best_ans(self,question:str, knowlege_base : dict) -> None:
        for i in knowlege_base["questions"]:
            if i["question"] == question:
                return i["answer"]
        return None
    def chat_bot(self):
        if self.runner or self.admin_access or self.admin_maker_combo:
            knowlege_base : dict= self.load_json('knowlege.json')
        
            while True:
                user_input,done = QtWidgets.QInputDialog.getText(
                self,
                'سوال؟',
                'سوال خود را وارد کنید.',
                
            )
                if not done:
                    return


                
                best_matche : str | None =self.best_matches(user_input, [i["question"] for i in knowlege_base["questions"]])
                if best_matche:
                    answer: str=self.get_best_ans(best_matche, knowlege_base)
                    QMessageBox.information(self,'جواب',f'{answer}')
                elif self.admin_access or self.admin_maker_combo:
                    QMessageBox.warning(self,'خطا',"من متوجه حرف شما نشدم می شه به من یاد بدهید")
                    new_answer,done2 = QtWidgets.QInputDialog.getText(
                    self,
                    'جواب',
                    'اگر می خواهید این سوال رد شود "skip" بنویسید در غیر اینصورت جواب دهید.',
                
                    )
                    if not done2:
                        return
                    lowed_new_ans = new_answer.lower()
                    if lowed_new_ans != 'skip':
                        knowlege_base["questions"].append({"question": user_input, "answer": lowed_new_ans})
                        self.save_knowlege('knowlege.json', knowlege_base)
                        QMessageBox.information(self,'موفقیت','متشکرم')
                else:
                     QMessageBox.warning(
                          self,
                          'خطا',
                          'من برای جواب دادن به این سوال طراحی نشدم.'
                     )
        else:
             QMessageBox.warning(
                  self,
                  'خطا',
                  'لطفا وارد شوید.'
             )

    def time_extend_email(self,now):
        
        # Check if each date in the list has already passed
        c.execute(
                            "SELECT giving_back FROM barrower"
                        )
        giving_back = c.fetchall()
        for left in giving_back:
            if now == left:
                        c.execute(
                                        "SELECT email FROM barrower WHERE giving_back=?", (now)
                                    )
                        email = c.fetchone()
                        for left2 in email:
                            self.email_alert('اتمام مهلت','لطفا کتاب هایی که قرض گرقتید را به کتابخانه تحویل دهید.\n .تشکر',left2)
                        break

            
    def changing_inventory_sum(self) :
        while True:
        #getting inputs
         book_name,done2 = QtWidgets.QInputDialog.getText(
              self,
              'کتاب',
              'نام کتاب را وارد کنید.',
              
         )
         if not done2:
              return
         if not book_name == '':
             break
        while True:
         numbers,done1 = QtWidgets.QInputDialog.getInt(
              self,
              'تعداد',
              'تعدادی که اضافه می شود را وارد کنید.',
              min=1
         )
         if not done1:
              return
         #adding books to inventory
         if not numbers == '':
             break
         
        c.execute('UPDATE book SET inventory=inventory+? WHERE name=?',(numbers, book_name))
        conn.commit()
        c.execute('UPDATE book SET inventory_unchangeable=inventory_unchangeable+? WHERE name=?',(numbers, book_name))
        conn.commit()
     #changin unchangable inventory minus
    def changing_inventory_minus(self) :
         #getting inputs
        while True:
         book_name,done2 = QtWidgets.QInputDialog.getText(
              self,
              'کتاب',
              'نام کتاب را وارد کنید.',
              
         )
         if not done2:
              return
         if not book_name == '':
             break
        while True:
         numbers,done1 = QtWidgets.QInputDialog.getInt(
              self,
              'تعداد',
              'تعدادی که کم می شود را وارد کنید.',
              min=1
         )
         if not done1:
              break
              return
         if not numbers == '':
             break
         #removing books from inventory
        c.execute('UPDATE book SET inventory=inventory-? WHERE name=?',(numbers, book_name))
        conn.commit()
        c.execute('UPDATE book SET inventory_unchangeable=inventory_unchangeable-? WHERE name=?',(numbers, book_name))
        conn.commit()    
     #making admin accounts  
    def admin_maker(self):
        if self.admin_maker_combo == True :
            while True:
                admin_name, done1 = QtWidgets.QInputDialog.getText(
                            self, "نام", "نام  خود را وارد کنید :"
                        )
                if not done1:
                        return  # User clicked "Cancel"
                if not admin_name == '':
                    break
            while True:
                admin_last_name, done3 = QtWidgets.QInputDialog.getText(
                            self, "فامیلی ", "نام خانوداگی خود را وارد کنید :"
                
                        )
                if not done3:
                    return  # User clicked "Cancel"
                if not admin_last_name == '':
                    break
            while True:
                user_name, done = QtWidgets.QInputDialog.getText(
                            self, "نام", "نام  خود را وارد کنید :"
                        )
                if not done:
                        return  # User clicked "Cancel"
                if not user_name == '':
                    break
                c.execute("SELECT user_name FROM admin_user")
                usr_name = c.fetchone()
                for i in usr_name:
                    if i == user_name:
                         QMessageBox.warning(
                              self,
                              'خطا',
                              'این نام کاربری از قبل استفاده شده'
                         )
            while True:
                National_code, done3 = QtWidgets.QInputDialog.getInt(
                            self, "کد ملی", " کد ملی خود را وارد کنید:",min = 100000000, max= 999999999
                
                        )
                if not done3:
                    return  # User clicked "Cancel"
                break
            while True:
                email,done4 = QtWidgets.QInputDialog.getText(
                    self,'ایمیل','ایمیل خود را وارد کنید.'
                )
                if not done4:
                    return
                if not email == '':
                    break
            while True:
                admin_password, done2 = QtWidgets.QInputDialog.getText(
                            self, "پسورد ادمین", " رمز اکانت خود را وارد کنید :", echo=QLineEdit.Password
                        )
                if not done2:
                            return  # User clicked "Cancel"
                if len(admin_password) >= 6:
                    break
            

            c.execute(
                        "INSERT INTO admin_user (name,password,last_name,National_Code,email,user_name) VALUES (?, ?, ?, ?, ?,?)",
                                (
                                    admin_name,
                                    admin_password,
                                    admin_last_name,
                                    National_code,
                                    email,
                                    user_name
                                ),
                            )
            conn.commit()
            QMessageBox.information(
                        self,
                        'موفقیت',
                        'شما با موفقیت اکانت ادمین خود را درست کردید'
            )
    #function for sending messages for email
    def email_alert(self, subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        user = "mahradmohamadinasab@gmail.com"
        msg['from'] = user
        password = 'zhtn jldu kqnl fjqj'
        server = SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        
        server.quit()
    
        
        
           
    # add book button function
    def add_book(self):

        
            if self.admin_combo == True:
                itemss = ['یک گزینه را انتخاب کنید','داستانی','درسی','رمان','طنز','تاریخی','اشعار']
                while True:
                    genre,done7 = QtWidgets.QInputDialog.getItem(self,'ژانر','ژانر کتاب را انتخاب کنید:',itemss)
                    if not done7:
                        return
                    if not genre == 'یک گزینه را انتخاب کنید':
                        break
                while True:
                    book_name, done1 = QtWidgets.QInputDialog.getText(
                        self, " کتاب", " نام کتاب را وارد کنید :"
                    )
                    if not done1:
                        return  # User clicked "Cancel"
                    #checking is the input having a letter or not
                    if not book_name == '':
                        break
                while True:
                    author_name, done2 = QtWidgets.QInputDialog.getText(
                        self, "نویسنده", " نام نویسنده را وارد کنید :"
                    )
                    if not done2:
                        return  # User clicked "Cancel"
                    #checking is the input having a letter or not
                    if not author_name == '':
                        break
                    
                    
                    
                while True:
                    translator_name, done3 = QtWidgets.QInputDialog.getText(
                        self, "مترجم", " نام مترجم را وارد کنید :\n اگر کتاب مترجم ندارد . وارد کنید"
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    #checking is the input having a letter or not
                    if translator_name == ".":
                        translator_name = "NONE"
                        break

                    elif not translator_name == '':
                        break
                while True:
                    
                    publisher, done4 = QtWidgets.QInputDialog.getText(
                        self, "ناشر", " نام ناشر را وارد کنید :\n اگر کتاب ناشر ندارد . وارد کنید"
                    )
                    if not done4:
                        return  # User clicked "Cancel"
                    if publisher == ".":
                        publisher = "NONE"
                        break
                    elif not publisher == '':
                        break
                    
                pages, done8 = QtWidgets.QInputDialog.getInt(
                    self, " کتاب", " تعداد صفحات کتاب را وارد کنید:",min=1
                )
                if not done8:
                    return  # User clicked "Cancel"

                publish_year, done5 = QtWidgets.QInputDialog.getInt(
                    self, "سال انتشار", " سال انتشار را وارد کنید :",max=2024,min=1
                )
                if not done5:
                    return  # User clicked "Cancel"
                inventory_unchangeable, done6 = QtWidgets.QInputDialog.getInt(
                    self, "تعداد", " تعداد را وارد کنید :",min=1
                )
                if not done6:
                    return  # User clicked "Cancel"

                inventory = inventory_unchangeable
                

                c.execute(
                    "INSERT INTO book (name, author, translator, publisher,publish_year, inventory,genre,pages,inventory_unchangeable) VALUES (?, ?, ?, ?, ?, ?,?,?,?)",
                    (
                        book_name,
                        author_name,
                        translator_name,
                        publisher,
                        publish_year,
                        inventory,
                        genre,
                        pages,
                        inventory_unchangeable,
                    ),
                )
                conn.commit()
                msg_box = QMessageBox()
                msg_box.setText("کتاب با موفقیت ذخیره شد!")
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("موفقیت")
                msg_box.exec_()
            else:
                QMessageBox.warning(
                    self, "اکانت ادمین لازم است", "لطفا با اکانت ادمین وارد شوید ."
                )
                return

    # exit button function
    def exitt(self):
        if self.runner:
            c.execute(
                                            "SELECT * FROM user WHERE name = ?", (self.current_user_name)
                                        )
            email = c.fetchone()
            rate = email[7]
            if rate != '1':
                while True:
                    items = ['لطفا امتیاز دهید.','1','2','3','4','5','بعدا']
                    answer, done = QtWidgets.QInputDialog.getItem(
                        self,
                        'نظر دهی.',
                        'لطفا امتیاز دهید.',
                        items
                    )
                    if not done:
                        exit()
                    if not answer == items[0]:
                        break
                self.email_alert('نظر دهی',f'نمره ای که به بر نامت دادن {answer} از {self.current_user_name} {email[2]} ','mahradmohamadinasab@gmail.com')  
                c.execute("UPDATE user SET rating = True WHERE name=? and password = ? and id = ?", (self.current_user_name, self.current_user_pass, self.logged_in_user_id))
                conn.commit()
        elif self.admin_combo:
             c.execute(
                        "SELECT * FROM admin_user WHERE name = ? and password = ?, id = ?", (self.current_user_name, self.current_user_pass, self.logged_in_user_id)
                                        )
             email = c.fetchone()
             if not email[7] == '1':
                while True:

                    items = ['لطفا امتیاز دهید.','1','2','3','4','5']
                    answer, done = QtWidgets.QInputDialog.getItem(
                        self,
                        'نظر دهی.',
                        'لطفا امتیاز دهید.',
                        items
                    )
                    if not done:
                        exit()
                    if not answer == items[0]:
                        break
                self.email_alert('نظر دهی',f'نمره ای که به بر نامت دادن {answer} از {self.current_user_name} {email[2]} ','mahradmohamadinasab@gmail.com')  
                c.execute("UPDATE admin_user SET rating = True WHERE name=? and password =?, id = ?", (self.current_user_name,self.current_user_pass, self.logged_in_user_id))
                conn.commit()
        exit()
    # remove book function
    def remove_book(self):
            
                if self.admin_combo == True:  #check is it admin account or not
                    while True:
                        book_name, done6 = QtWidgets.QInputDialog.getText(
                            self, "کتاب", "اسم کتاب پس داده شده را وارد کنید: "
                        )
                        if not done6:
                            return  # User clicked "Cancel"
                        if not book_name == '':
                            
                            c.execute("SELECT * FROM bo WHERE name=?", (book_name,))
                            Inventory = c.fetchone()

                            c.execute("UPDATE book SET user_id=NULL WHERE name=?", (book_name,))
                            if Inventory[6] < Inventory[9]:
                                c.execute("UPDATE book SET inventory=inventory+1 WHERE name=?", (book_name,))
                                c.execute('DELETE FROM barrower WHERE id=?', (book_name,))
                            else:
                                QMessageBox.warning(
                                    self,
                                    'بیشتر از حداکثر',
                                    f'تعداد کتاب های  {book_name} با تعداد کتاب های تعیین شده برابر است و نمی توان ان را بیشتر کرد.'
                                )
                                return

                            conn.commit()
                            msg_box1 = QMessageBox()
                            msg_box1.setText("کتاب با موفقیت پس داده شد!")
                            msg_box1.setIcon(QMessageBox.Information)
                            msg_box1.setWindowTitle("Success")
                            msg_box1.exec_()
                            break
                        
                    
                else:
                    QMessageBox.warning(
                        self, "نیاز به اکانت ادمین است", " لطفا با اکانت ادمین وارد شوید."
                    )
                    return

    #showing all the books     
    def show_books(self):
        
            c.execute("SELECT * FROM book")
            books = c.fetchall()

            book_info = ""
            for book in books:
                book_info += f"    ایدی کتاب: {book[0]}\n    ژانر: {book[7]}\n    اسم کتاب: {book[1]}\n    نویسنده: {book[2]}\n    مترجم: {book[3]}\n    ناشر: {book[4]}\n    تعداد صفحات:{book[8]}\n    سال انتشار: {book[5]}\n    تعداد  : {book[6]}\n    ========================\n\n"
            dialog = QDialog(self)
            dialog.setWindowTitle("اطلاعات کتاب ها")

            scroll_area = QScrollArea(dialog)
            scroll_area.setWidgetResizable(True)

            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)

            label = QLabel(book_info, parent=dialog)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_layout.addWidget(label)

            scroll_area.setWidget(content_widget)

            layout = QVBoxLayout(dialog)
            layout.addWidget(scroll_area)

            dialog.exec_()
    #making account function
    def sign_up(self):
        
            while True:
                # New user registration
                name, done1 = QtWidgets.QInputDialog.getText(
                    self, "ثبت نام", "اسم خود را وارد کنید : "
                    )
                
                
                if not done1:
                    return  # User clicked "Cancel"
                if not name == '':
                    c.execute("SELECT name  FROM user")
                    name = c.fetchone
                    for i in name:
                         if i == name:
                              QMessageBox.warning(
                                   self,
                                   'خطا',
                                   'این نام کاربری قبلا استفاده شده.'
                              )
                    break
            while True:
                user_name, doneee = QtWidgets.QInputDialog.getText(
                            self, "نام", "نام  خود را وارد کنید :"
                        )
                if not doneee:
                        return  # User clicked "Cancel"
                if not user_name == '':
                    break
            while True:
                user_last_name, done = QtWidgets.QInputDialog.getText(
                    self, "ثبت نام", " فامیلی خود را وارد کنید : "
                    )
                
                if not done:
                    return  # User clicked "Cancel"
                if not user_last_name == '':
                    break
            international_code, donee = QtWidgets.QInputDialog.getInt(
                self, "ثبت نام", "کد ملی خود را وارد کنید : ", min=100000000, max=999999999
                )
            
            if not donee:
                return  # User clicked "Cancel"
            grade_ = ['پایه خود را وارد کنید','اول','دوم','سوم','چهارم','پنجم','ششم','هفتم','هشتم','نهم','دهم','یازدهم','دوزدهم','فوق دیپلم','لیسانس','فوق لیسانس','دکترا','فوق دکترا','شاغل']
            while True:
                grade, done2 = QtWidgets.QInputDialog.getItem(
                    self, "ثبت نام", "پایه خود را وارد کنید : ",grade_
                )
                if not done2:
                    return  # User clicked "Cancel"
                if not grade == 'پایه خود را وارد کنید':
                     break
            classes1 = ['کلاس خود را وارد کنید','1/1','1/2','1/3','1/4']
            classes2 = ['کلاس خود را وارد کنید','2/1','2/2','2/3','2/4']
            classes3 = ['کلاس خود را وارد کنید','3/1','3/2','3/3','3/4']
            classes4 = ['کلاس خود را وارد کنید','4/1','4/2','4/3','4/4']
            classes5 = ['کلاس خود را وارد کنید','5/1','5/2','5/3','5/4']
            classes6 = ['کلاس خود را وارد کنید','6/1','6/2','6/3','6/4']
            classes7 = ['کلاس خود را وارد کنید','7/1','7/2','7/3','7/4']
            classes8 = ['کلاس خود را وارد کنید','8/1','8/2','8/3','8/4']
            classes9 = ['کلاس خود را وارد کنید','9/1','9/2','9/3','9/4']
            classes10 = ['کلاس خود را وارد کنید','10/1','10/2','10/3','10/4']
            classes11 = ['کلاس خود را وارد کنید','11/1','11/2','11/3','11/4']
            classes12 = ['کلاس خود را وارد کنید','12/1','12/2','12/3','12/4']
            while True:
                if grade == grade_[1]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes1
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[2]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes2
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[3]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes3
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[4]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes4
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[5]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes5
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[6]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes6
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[7]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes7
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_ [8]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes8
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[9]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes9
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[10]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes10
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[11]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes11
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                elif grade == grade_[12]:
                    user_cls, done3 = QtWidgets.QInputDialog.getItem(
                        self, "ثبت نام", "شماره کلاس خود را وارد کنید: ", classes12
                    )
                    if not done3:
                        return  # User clicked "Cancel"
                    if not user_cls == 'کلاس خود را وارد کنید':
                        break
                user_cls = 'NONE'
                break

            while True:
                    email,done4 = QtWidgets.QInputDialog.getText(
                    self,'ایمیل','ایمیل خود را وارد کنید.'
                    )
                    
                    if not done4:
                        return
                    if not email == '':
                        email_cheker = email.split('@')
                        if not email_cheker[0] == '':
                            if email_cheker=='gmail.com'or email_cheker=='yahoo.com'or email_cheker=='outlook.com':
                                code = randint(100000, 999999)
                                self.email_alert('ایمیل',f'کد ساخت اکانت {str(code)}',email)
                                inp_code = QtWidgets.QInputDialog.getInt(self,'کد',':کد فرستاده شده را وارد کنید.')
                                if str(code) == str(inp_code):
                                    break
                                else:
                                    QMessageBox.warning(self,'خطا','کد وارد شده اشتباه است')
                            else:
                                 QMessageBox.warning(self,'خطا','لطفا ایمیل واقعی خود را وارد کنید.')
                        else:
                            QMessageBox.warning(self,'خطا','لطفا ایمیل خود را وارد کنید.')
            while True:
                    password, done4 = QtWidgets.QInputDialog.getText(
                        self, "ثبت نام", "پسورد خود را وارد کنید : ", echo=QLineEdit.Password
                    )
                    if not done4:
                        return  # User clicked "Cancel"  
                    if len(password) >= 6:
                        break
                    else:
                         QMessageBox.warning(
                              self,
                              'خطا',
                              'لطفا پسورد خود را حداقل تا 6 حرف درست کنید.'
                         )
                

            c.execute(
                    "INSERT INTO user (name, grade, class,last_name,National_Code, password,email,rating,user_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_name, grade, user_cls,user_last_name,international_code, password,email,'False', user_name),
                )
            conn.commit()

            msg_box = QMessageBox()
            msg_box.setText("شما با موفقیت ثبت نام کردید!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("موفقیت")
            msg_box.exec_()
            choice =  QMessageBox.question(self, "ورود??", 
                                            '''ایا می خواهید وارد شوید🤔🤔''',
                                            QMessageBox.Yes | QMessageBox.No)
            
                
        
        
            if choice == QMessageBox.Yes:

                c.execute("SELECT id FROM user WHERE name=?", (user_name,))
                usr_id = c.fetchone()
                self.logged_in_user_id = usr_id[0]
                self.current_user_name = user_name
                self.current_user_pass = password
                self.runner = True

                opacity_effect_normal = QGraphicsOpacityEffect() 
                opacity_effect2 = QGraphicsOpacityEffect() 
                opacity_effect3 = QGraphicsOpacityEffect() 
                                # setting opacity level 

                opacity_effect_normal.setOpacity(100) 
            

                self.normal_combobox.setGraphicsEffect(opacity_effect_normal)
                self.normal_combobox.setEnabled(True)
                self.normal_combobox.setGeometry(70, 10, 91, 41 )
                self.normal_combo = True

                opacity_effect2.setOpacity(0) 

                                    # adding opacity effect to the label 
                self.login.setGraphicsEffect(opacity_effect2)
                self.login.setGeometry(10, 440, 101, 28)  
                self.login.setEnabled(False)

                opacity_effect3.setOpacity(0) 
                                    # adding opacity effect to the label 
                self.sign__up.setGraphicsEffect(opacity_effect3)
                self.sign__up.setGeometry(120, 440, 101, 28)  
                self.sign__up.setEnabled(False)

                opacity_effect4 = QGraphicsOpacityEffect() 
                opacity_effect4.setOpacity(0)
                self.admin__maker.setGraphicsEffect(opacity_effect4)
                self.admin__maker.setEnabled(False)
    
    

    #barrowing books
    def borrow_book(self):
        
            
        
            if self.admin_combo or self.admin_maker_combo:
                QMessageBox.warning(
                    self, "درسرسی ندارید", "لطفا با اکانت عادی وارد شوید ."
                )
                return
            elif self.runner == False:
                QMessageBox.warning(
                    self, "ورود کنید", "لطفا وارد شوید تا بتوانید این کار را انجام دهید ."
                )
                return
            
            else:
                while True:
                    book_name, done7 = QtWidgets.QInputDialog.getText(
                        self, "کتاب", "اسم کتاب را وارد کنید تا قرض گرفته شود : "
                    )
                    if not done7:
                        return  # User clicked "Cancel"
                    if not book_name == '':

                    # Check if the book exists and if there are available copies
                        c.execute("SELECT * FROM book WHERE name=?", (book_name,))
                        inventory = c.fetchone()
                        if not inventory:
                            QMessageBox.warning(
                                self, "کتاب پیدا نشد", "کتابی که شما وارد کردید در کتابخانه نداریم."
                            )
                            return
                        if inventory[6] <= 0:
                            QMessageBox.warning(
                                self,
                                "موجود نیست",
                                "این کتاب موجود نیست .",
                            )
                            return
                        #seeing when user will give back the book 
                        back_time, done1 = QtWidgets.QInputDialog.getInt(
                            self, "کتاب", "تا چند روز دگر پس می دهید:",step=7,min=0,max=14
                        )
                        if not done1:
                            return  # User clicked "Cancel"
                        if back_time == 0:
                            QMessageBox.information(
                                self,
                                'متاسفانه',
                                'به دلیل وارد نکردن مقدار زمانی که پس می دهید برای شما 2 هفته حساب شده است'
                            )
                            back_time = 14

                        c.execute(
                            "UPDATE book SET user_id=?  WHERE name=?",
                            (self.logged_in_user_id, book_name),
                        )
                        c.execute("UPDATE book SET inventory=inventory-1 WHERE name=?", (book_name,))

                        conn.commit()
                        QMessageBox.information(
                            self, "کتاب قرض گرفته شد", "شما با موفقیت کتاب را قرض گرفتید ."
                        )
                        c.execute("SELECT * FROM user WHERE name=? ", (self.current_user_name,))
                        account_info = c.fetchone()

                        c.execute("SELECT * FROM book WHERE name=?", (book_name,))
                        books = c.fetchone()
                        # Create a datetime object (automate)
                        start_date = date.today()

                        # Add 5 days to the start date
                        end_date = start_date + timedelta(days=back_time)

                        # Format the end date as "yyyy/mm/dd"
                        formatted_date = end_date.strftime("%Y/%m/%d")



                        c.execute(
                            "INSERT INTO barrower (genre,name, author, translator, publisher,publish_year,name_user,last_name,grade, class, user_id,pages, giving_back, email, user_name) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                books[7],
                                book_name,
                                books[2],   
                                books[3],
                                books[4],
                                books[5],
                                account_info[1],
                                account_info[2],
                                account_info[5],
                                account_info[6],
                                account_info[0],
                                books[8],
                                formatted_date,
                                account_info[9],
                                account_info[3]
                            ),
                        )
                        conn.commit()
                        break

    #loggining in to account
    def log_in(self):
            choice =  QMessageBox.question(self, "ورود??", 
                                           '''ایا شما اکانت ادمین دارید''',
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Cancel:
                 return

            while True:
                 
                    user_name, done7 = QtWidgets.QInputDialog.getText(
                    self, "ورود", "اسم اکانت را وارد کنید : "
                        )
                    if not done7:
                            return  # User clicked "Cancel"
                    if not user_name == '' :
                        break
            while True:
                    password, done8 = QtWidgets.QInputDialog.getText(
                            self, "ورود", "پسورد خود را وارد کنید : ", echo=QLineEdit.Password
                        )
                    if not done8:
                            return  # User clicked "Cancel"
                    if not password == '':
                        break
            choice = QMessageBox.question(
                     self,
                     'سوال؟',
                     'دوست دارید رمز خود را ببینید؟',
                    QMessageBox.Yes | QMessageBox.No
                )
            if choice == QMessageBox.Yes:
                     QMessageBox.information(self,'رمز',f'رمز شما : {password} ')
                     choice = QMessageBox.question(
                                                     self,
                                                     'سوال',
                                                     'آیا رمز شما درست است؟',
                                                     QMessageBox.Yes | QMessageBox.No
                                                )
                     if choice == QMessageBox.No:
                                                while True:
                                                    password, done9 = QtWidgets.QInputDialog.getText(
                                                    self, "ورود", "پسورد جدید خود را وارد کنید: "
                                                    )
                                                    if not done9:
                                                        return  # User clicked "Cancel"
                                                    
                                                    if len(password) < 6 :
                                                        QMessageBox.warning(
                                                            self,
                                                            'تعداد حروف کم',
                                                            'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                        )
                                                    if len(password2) >= 6:
                                                        break
                                                    choice = QMessageBox.question(
                                                    self,
                                                    'سوال؟',
                                                    'دوست دارید رمز خود را ببینید؟',
                                                    QMessageBox.Yes | QMessageBox.No
                                                    )
                                                    if choice == QMessageBox.Yes:
                                                        QMessageBox.information(self,'رمز',f'رمز شما : {password} ')   
            if choice == QMessageBox.No :
                
                    
                    # Check if username and password match in the database
                c.execute(
                            "SELECT * FROM user WHERE user_name=? AND password=?", (user_name, password)
                        )
                user = c.fetchone()
                if user:
                    self.logged_in_user = user_name
                    c.execute("SELECT id FROM user WHERE user_name=?", (self.logged_in_user,))
                    usr_id = c.fetchone()
                    self.logged_in_user_id = usr_id[0]
                    QMessageBox.information(
                                self,
                                "با موفقیت ",
                                f'''سلام دوست من
شما به عنوان {user_name} وارد شدید''',
                            )

                    self.current_user_name = user_name
                    
                    
                    self.current_user_pass = password
                    
                    

                    opacity_effect_normal = QGraphicsOpacityEffect() 
                    opacity_effect_normal.setOpacity(100) 

                # adding opacity effect to the label 
                    self.normal_combobox.setGraphicsEffect(opacity_effect_normal)
                    self.normal_combobox.setEnabled(True)
                    self.normal_combobox.setGeometry(70, 10, 91, 41 )
                    self.normal_combo = True
                    self.runner = True


                    opacity_effect2 = QGraphicsOpacityEffect() 

                            # setting opacity level log in
                    opacity_effect2.setOpacity(0) 

                            # adding opacity effect to the label 
                    self.login.setGraphicsEffect(opacity_effect2)
                    self.login.setGeometry(10, 440, 101, 28)  
                    self.login.setEnabled(False)
                    opacity_effect3 = QGraphicsOpacityEffect() 

                            # setting opacity level sign in
                    opacity_effect3.setOpacity(0) 

                            # adding opacity effect to the label 
                    self.sign__up.setGraphicsEffect(opacity_effect3)
                    self.sign__up.setGeometry(120, 440, 101, 28)  
                    self.sign__up.setEnabled(False)
                    
                    opacity_effect4 = QGraphicsOpacityEffect() 
                    opacity_effect4.setOpacity(0)
                    self.admin__maker.setGraphicsEffect(opacity_effect4)
                    self.admin__maker.setEnabled(False)
                    #setting Geometry
            
                else:
                            choice = QMessageBox.question(self, "فراموشی رمز", 
                                                '''به نظر می رسه شما رمز خود را فراموش کرده اید!!
        می خواهید تغییرش بدهید ؟''',
                                                QMessageBox.Yes | QMessageBox.No)
                            if choice == QMessageBox.Yes:

                                random_choice = randint(100000,999999)
                                random_choice = str(random_choice)
                                
                                c.execute(
                                "SELECT email FROM user WHERE user_name=?", (user_name)
                                )
                                user = c.fetchone()
                                self.email_alert("تغییر رمز",f'کد یک بار مصرف :{random_choice}',user)
                                cheking, done10 = QtWidgets.QInputDialog.getInt(self,'تغییر رمز','لطفا عدد پیامک شده به ایمیل خود را ثبت کنید:')
                                if not done10:
                                        return
                                if str(cheking) == random_choice:
                                    while True:
                                        new_password, done9 = QtWidgets.QInputDialog.getText(
                                            self, "ورود", "پسورد جدید خود را وارد کنید: "
                                        )
                                        if not done9:
                                            return  # User clicked "Cancel"
                                        if len(new_password) < 6 :
                                                QMessageBox.warning(
                                                    self,
                                                    'تعداد حروف کم',
                                                    'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                )
                                        if len(new_password) >= 6 :
                                                break
                                        choice = QMessageBox.question(
                                            self,
                                            'سوال؟',
                                            'دوست دارید رمز خود را ببینید؟',
                                            QMessageBox.Yes | QMessageBox.No
                                        )
                                        if choice == QMessageBox.Yes:
                                            QMessageBox.information(self,'رمز',f'رمز شما : {new_password} ')
                                            choice = QMessageBox.question(
                                                     self,
                                                     'سوال',
                                                     'آیا رمز شما درست است؟',
                                                     QMessageBox.Yes | QMessageBox.No
                                                )
                                            if choice == QMessageBox.No:
                                                    while True:
                                                        new_password, done9 = QtWidgets.QInputDialog.getText(
                                                        self, "ورود", "پسورد جدید خود را وارد کنید: "
                                                        )
                                                        if not done9:
                                                            return  # User clicked "Cancel"
                                                        
                                                        if len(new_password) < 6 :
                                                            QMessageBox.warning(
                                                                self,
                                                                'تعداد حروف کم',
                                                                'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                            )
                                                        if len(new_password) >= 6:
                                                            break
                                                        choice = QMessageBox.question(
                                                        self,
                                                        'سوال؟',
                                                        'دوست دارید رمز خود را ببینید؟',
                                                        QMessageBox.Yes | QMessageBox.No
                                                        )
                                                        if choice == QMessageBox.Yes:
                                                            QMessageBox.information(self,'رمز',f'رمز شما : {new_password} ')
                                    while True:
                                        new_password2, done9 = QtWidgets.QInputDialog.getText(
                                            self, "ورود", "پسورد جدید خود را وارد کنید: ",echo=QLineEdit.password
                                        )
                                        if not done9:
                                            return  # User clicked "Cancel"
                                        if not new_password2 == '':
                                            break
                                        choice = QMessageBox.question(
                                            self,
                                            'سوال؟',
                                            'دوست دارید رمز خود را ببینید؟',
                                            QMessageBox.Yes | QMessageBox.No
                                        )
                                        if choice == QMessageBox.Yes:
                                            QMessageBox.information(self,'رمز',f'رمز شما : {new_password2} ')
                                            choice = QMessageBox.question(
                                                     self,
                                                     'سوال',
                                                     'آیا رمز شما درست است؟',
                                                     QMessageBox.Yes | QMessageBox.No
                                                )
                                            if choice == QMessageBox.No:
                                                    new_password2, done9 = QtWidgets.QInputDialog.getText(
                                                    self, "ورود", "پسورد جدید خود را وارد کنید: "
                                                    )
                                                    if not done9:
                                                        return  # User clicked "Cancel"
                                                    
                                                    if len(new_password2) < 6 :
                                                        QMessageBox.warning(
                                                            self,
                                                            'تعداد حروف کم',
                                                            'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                        )
                                                    if len(new_password2) >= 6:
                                                        break
                                                    choice = QMessageBox.question(
                                                    self,
                                                    'سوال؟',
                                                    'دوست دارید رمز خود را ببینید؟',
                                                    QMessageBox.Yes | QMessageBox.No
                                                    )
                                                    if choice == QMessageBox.Yes:
                                                        QMessageBox.information(self,'رمز',f'رمز شما : {new_password2} ')
                                    
                                    if new_password2 == new_password:
                                        
                                        QMessageBox.information(
                                        self,
                                        "موفقیت",
                                        '''عالی!!😁😁
            رمز شما با موفقیت تغییر کرد''',
                                        )
                                        c.execute("UPDATE user SET password=? WHERE user_name=?", (new_password2,user_name))
                                        conn.commit
                                    else:
                                        QMessageBox.warning(
                                            self,
                                            'اشتباه',
                                            ''
                                        )
                                else:
                                     QMessageBox.warning(
                                          self,
                                          'غلط',
                                          'کد پیامک شده برای شما این نیست.'

                                     )
                            elif choice ==QMessageBox.No :
                                QMessageBox.warning(
                                self,
                                "ارور",
                                '''پسورد شما اشتباه هست''',
                            )
            else:

                if user_name == "mahrad" and password == "mahrad1390":
                    while True:
                             password2, done11 = QtWidgets.QInputDialog.getText(
                            self, "ورود", "پسورد دوم این اکانت را هم وارد کنید : ", echo=QLineEdit.Password
                                        )
                             if not done11:
                                return 
                             if not password2 == '':
                                break
                             choice = QMessageBox.question(
                                            self,
                                            'سوال؟',
                                            'دوست دارید رمز خود را ببینید؟',
                                            QMessageBox.Yes | QMessageBox.No
                                        )
                             if choice == QMessageBox.Yes:
                                            QMessageBox.information(self,'رمز',f'رمز شما : {password} ')
                             
                    if password2 == "MAHRAD1390.2024":
                                QMessageBox.information(
                                   self,
                                   'کار این اکانت' ,
                                   "شما با این اکانت تنها می توانید اکانت ادمین بسازید"
                                )

                                self.admin_maker_combo = True
                                opacity_effect2 = QGraphicsOpacityEffect() 

                                # setting opacity level log in
                                opacity_effect2.setOpacity(0) 

                                # adding opacity effect to the label 
                                self.login.setGraphicsEffect(opacity_effect2)
                                self.login.setGeometry(10, 440, 101, 28)  
                                self.login.setEnabled(False)

                                opacity_effect_admin_maker2 = QGraphicsOpacityEffect()
                                opacity_effect_admin_maker2.setOpacity(10)
                                self.admin__maker.setGraphicsEffect(opacity_effect_admin_maker2)
                                self.admin__maker.setEnabled(True)
                                self.admin__maker.setGeometry(120, 20, 101, 28)  
                                opacity_effect3 = QGraphicsOpacityEffect() 

                                # setting opacity level sign in
                                opacity_effect3.setOpacity(0) 

                                # adding opacity effect to the label 
                                self.sign__up.setGraphicsEffect(opacity_effect3)
                                self.sign__up.setGeometry(120, 440, 101, 28)  
                                self.sign__up.setEnabled(False)
                                opacity_effect_ADMIN = QGraphicsOpacityEffect() 
                                opacity_effect_ADMIN.setOpacity(100) 

                    # adding opacity effect to the label 
                                self.admin_combobox.setGraphicsEffect(opacity_effect_ADMIN)
                                self.admin_combobox.setEnabled(True)
                                self.admin_combobox.setGeometry(10, 10, 91, 41 )

                        
                                
                    else:
                                QMessageBox.warning(
                                    self,
                                    'اشتباه',
                                    'رمز دوم این اکانت اشتباه است'
                                )
                                


                                
                        
                

                else:
                    # Check if username and password match in the database
                            
                            c.execute(
                                        "SELECT * FROM admin_user WHERE user_name=? AND password=?", (user_name, password)
                                    )
                            user = c.fetchone()
                            if user:
                                    self.logged_in_user = user_name
                                    c.execute("SELECT id FROM admin_user WHERE user_name=?", (self.logged_in_user,))
                                    usr_id = c.fetchone()
                                    self.logged_in_user_id = usr_id[0]
                                    QMessageBox.information(
                                        self,
                                        "با موفقیت ",
                                        f'''سلام دوست من
    شما به عنوان {user_name} وارد شدید''',
                                    )

                                    self.current_user_name = user_name
                                    c.execute(
                                    "SELECT last_name FROM admin_user WHERE user_name=? AND password=?", (user_name, password)
                                    )
                                    user = c.fetchone()
                                    self.current_user_pass = password
                                    self.admin_combo = True

                                    opacity_effect_normal = QGraphicsOpacityEffect() 
                                    opacity_effect_normal.setOpacity(100) 

                        # adding opacity effect to the label 
                                    self.admin_combobox.setGraphicsEffect(opacity_effect_normal)
                                    self.admin_combobox.setEnabled(True)
                                    self.admin_combobox.setGeometry(10, 10, 91, 41 )

                                    opacity_effect_admin_maker = QGraphicsOpacityEffect()
                                    opacity_effect_admin_maker.setOpacity(0)
                                    self.admin__maker.setGraphicsEffect(opacity_effect_admin_maker)

                                    
                                    


                                    opacity_effect2 = QGraphicsOpacityEffect() 

                                    # setting opacity level log in
                                    opacity_effect2.setOpacity(0) 

                                    # adding opacity effect to the label 
                                    self.login.setGraphicsEffect(opacity_effect2)
                                    self.login.setGeometry(10, 440, 101, 28)  
                                    self.login.setEnabled(False)
                                    opacity_effect3 = QGraphicsOpacityEffect() 

                                    # setting opacity level sign in
                                    opacity_effect3.setOpacity(0) 

                                    # adding opacity effect to the label 
                                    self.sign__up.setGraphicsEffect(opacity_effect3)
                                    self.sign__up.setGeometry(120, 440, 101, 28)  
                                    self.sign__up.setEnabled(False)

                                    opacity_effect_inventory_sum = QGraphicsOpacityEffect()
                                    opacity_effect_inventory_minus = QGraphicsOpacityEffect()
                                    #percent of opacity
                                    opacity_effect_inventory_sum.setOpacity(100)
                                    opacity_effect_inventory_minus.setOpacity(100)

                                    #seting opacity's 
                                    self.changing__inventory_sum.setGraphicsEffect(opacity_effect_inventory_sum)
                                    self.changing__inventory_minus.setGraphicsEffect(opacity_effect_inventory_minus)
                                    #Enabling buttons
                                    self.changing__inventory_minus.setEnabled(True)
                                    self.changing__inventory_sum.setEnabled(True)
                                    #setting geometry
                                    self.changing__inventory_minus.setGeometry(275, 20, 141, 28)
                                    self.changing__inventory_sum.setGeometry(120, 20, 141, 28)

                            else:
                                choice = QMessageBox.question(
                                     self,
                                     'اشتباه',
                                     ' ایا می خواید پسورد خود را عوض کنید؟ ',
                                     QMessageBox.Yes | QMessageBox.No
                                )
                                if choice == QMessageBox.Yes:
                                    random_choice = randint(100000,999999)
                                    random_choice = str(random_choice)
                                    c.execute(
                                    "SELECT email FROM admin_user WHERE user_name=?", (user_name)
                                    )
                                    user = c.fetchone()
                                    self.email_alert("تغییر رمز",f'کد یک بار مصرف :{random_choice}',user)

                                    cheking, done10 = QtWidgets.QInputDialog.getInt(self,'تغییر رمز','لطفا عدد پیامک شده به ایمیل خود را ثبت کنید:',min=100000,max=999999)
                                        
                                    if not done10:
                                            return
                                        
                                    if str(cheking) == random_choice:
                                        while True:
                                            new_password, done9 = QtWidgets.QInputDialog.getText(
                                            self, "ورود", "پسورد جدید خود را وارد کنید: "
                                            )
                                            if not done9:
                                                return  # User clicked "Cancel"
                                            
                                            if len(new_password) < 6 :
                                                QMessageBox.warning(
                                                    self,
                                                    'تعداد حروف کم',
                                                    'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                )
                                            if len(new_password) >= 6:
                                                break
                                            choice = QMessageBox.question(
                                            self,
                                            'سوال؟',
                                            'دوست دارید رمز خود را ببینید؟',
                                            QMessageBox.Yes | QMessageBox.No
                                        )
                                            if choice == QMessageBox.Yes:
                                                QMessageBox.information(self,'رمز',f'رمز شما : {password} ')
                                                choice = QMessageBox.question(
                                                     self,
                                                     'سوال',
                                                     'آیا رمز شما درست است؟',
                                                     QMessageBox.Yes | QMessageBox.No
                                                )
                                                if choice == QMessageBox.No:
                                                    new_password, done9 = QtWidgets.QInputDialog.getText(
                                                    self, "ورود", "پسورد جدید خود را وارد کنید: "
                                                    )
                                                    if not done9:
                                                        return  # User clicked "Cancel"
                                                    
                                                    if len(new_password) < 6 :
                                                        QMessageBox.warning(
                                                            self,
                                                            'تعداد حروف کم',
                                                            'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                        )
                                                    if len(new_password) >= 6:
                                                        break
                                                    choice = QMessageBox.question(
                                                    self,
                                                    'سوال؟',
                                                    'دوست دارید رمز خود را ببینید؟',
                                                    QMessageBox.Yes | QMessageBox.No
                                                    )
                                                    if choice == QMessageBox.Yes:
                                                        QMessageBox.information(self,'رمز',f'رمز شما : {password} ')
                                        while True:
                                            new_password2, done9 = QtWidgets.QInputDialog.getText(
                                                self, "ورود", "پسورد جدید خود را وارد کنید: ",echo=QLineEdit.password
                                            )
                                            if not done9:
                                                return  # User clicked "Cancel"
                                            if not new_password2 == '':
                                                break
                                        choice = QMessageBox.question(
                                            self,
                                            'سوال؟',
                                            'دوست دارید رمز خود را ببینید؟',
                                            QMessageBox.Yes | QMessageBox.No
                                        )
                                        if choice == QMessageBox.Yes:
                                                QMessageBox.information(self,'رمز',f'رمز شما : {password} ')
                                                choice = QMessageBox.question(
                                                     self,
                                                     'سوال',
                                                     'آیا رمز شما درست است؟',
                                                     QMessageBox.Yes | QMessageBox.No
                                                )
                                                if choice == QMessageBox.No:
                                                    while True:
                                                        new_password2, done9 = QtWidgets.QInputDialog.getText(
                                                        self, "ورود", "پسورد جدید خود را وارد کنید: "
                                                        )
                                                        if not done9:
                                                            return  # User clicked "Cancel"
                                                        
                                                        if len(new_password2) < 6 :
                                                            QMessageBox.warning(
                                                                self,
                                                                'تعداد حروف کم',
                                                                'لطفا رمز خود را بیشتر از 6 حرف بنویسسد'
                                                            )
                                                            continue
                                                        if len(new_password2) >= 6:
                                                            break
                                                    choice = QMessageBox.question(
                                                        self,
                                                        'سوال؟',
                                                        'دوست دارید رمز خود را ببینید؟',
                                                        QMessageBox.Yes | QMessageBox.No
                                                        )
                                                    if choice == QMessageBox.Yes:
                                                            QMessageBox.information(self,'رمز',f'رمز شما : {password} ')
                                        if new_password == new_password2:
                                            QMessageBox.information(
                                                self,
                                                "موفقیت",
                                                '''عالی!!😁😁
رمز شما با موفقیت تغییر کرد''',
                                                )
                                            c.execute("UPDATE admin_user SET password=? WHERE user_name=?", (new_password2,user_name))
                                            conn.commit()
                                else:
                                     QMessageBox.warning(
                                          self,
                                          'اشتباه',
                                          'رمز عبور اشتباه است.'
                                     )
    #showing all the barrowed books                    
    def list_of_borrowed_books(self):
            if self.runner == True or self.admin_combo ==True or self.admin_maker_combo == True:
                c.execute("SELECT * FROM barrower")
                books = c.fetchall()

                book_info = ""
                for book in books:
                    book_info += f"    ایدی کتاب: {book[0]}\n    ژانر کتاب: {book[10]}\n    اسم کتاب: {book[5]}\n    نویسنده: {book[6]}\n    مترجم: {book[7]}\n    ناشر: {book[8]}\n    صفحات:{book[11]}\n    سال انتشار: {book[9]}\n     قرض گیرنده: {book[1]} {book[2]}\n     پایه : {book[3]}\n     کلاس : {book[4]}\n     تاریخ پس دادن کتاب : {book[14]}\n     ========================\n\n"
                dialog = QDialog(self)
                dialog.setWindowTitle("اطلاعات کتاب ها")

                scroll_area = QScrollArea(dialog)
                scroll_area.setWidgetResizable(True)

                content_widget = QWidget()
                content_layout = QVBoxLayout(content_widget)

                label = QLabel(book_info, parent=dialog)
                label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                content_layout.addWidget(label)

                scroll_area.setWidget(content_widget)

                layout = QVBoxLayout(dialog)
                layout.addWidget(scroll_area)

                dialog.exec_()

            else:
                    QMessageBox.warning(
                        self, "نیاز به ورود", "لطفا وارد شوید تا این کار را جلو ببریم ."
                    )
                    return
            
    #showing all the removed books
    def list_of_removed_books(self):
        
            
            if  self.runner == True or self.admin_access==True or self.admin_maker_combo == True:
                
                c.execute("SELECT * FROM book")
                books = c.fetchall()

                book_info = ""
                for book in books:
                    book_info += f"    ایدی کتاب: {book[0]}\n    اسم کتاب: {book[1]}\n    نویسنده: {book[2]}\n    مترجم: {book[3]}\n    ناشر: {book[4]}\n    سال انتشار: {book[5]}\n    تعداد: {book[6]}\n    ========================\n\n"
                dialog = QDialog(self)
                dialog.setWindowTitle("Book Information")

                scroll_area = QScrollArea(dialog)
                scroll_area.setWidgetResizable(True)

                content_widget = QWidget()
                content_layout = QVBoxLayout(content_widget)

                label = QLabel(book_info, parent=dialog)
                label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                content_layout.addWidget(label)

                scroll_area.setWidget(content_widget)

                layout = QVBoxLayout(dialog)
                layout.addWidget(scroll_area)

                dialog.exec_()
            else:
                QMessageBox.warning(
                    self, "وارد شوید", "لطفا وارد شوید تا این عملیات جلو برود ."
                )
                return
    #combo boxes action
    def combo_box_action(self):
        

        if self.normal_combobox.currentText() == "خروج از اکانت" or self.admin_combobox.currentText() == "خروج از اکانت":
            QMessageBox.information(
                self,
                "موفقیت",
                '''با موفقیت از اکانت خارج شدید''',
            )

            self.admin_combo = False
            self.admin_maker_combo = False
            self.runner = False

            opacity_effect2 = QGraphicsOpacityEffect()
            opacity_effect2.setOpacity(1.0)
            self.login.setGraphicsEffect(opacity_effect2)
            self.login.setGeometry(10, 20, 101, 28)
            self.login.setEnabled(True)
            opacity_effect3 = QGraphicsOpacityEffect()
            opacity_effect3.setOpacity(1.0)
            self.sign__up.setGraphicsEffect(opacity_effect3)
            self.sign__up.setGeometry(120, 20, 101, 28)
            self.sign__up.setEnabled(True)
            opacity_effect5 = QGraphicsOpacityEffect()
            opacity_effect5.setOpacity(0)
            self.admin_combobox.setGraphicsEffect(opacity_effect5)
            self.admin_combobox.setEnabled(False)
            self.admin_combobox.setGeometry(110, 440, 91, 41)
            self.admin_combobox.setCurrentIndex(0)
            opacity_effect4 = QGraphicsOpacityEffect()
            opacity_effect4.setOpacity(0)
            self.normal_combobox.setGraphicsEffect(opacity_effect4)
            self.normal_combobox.setEnabled(False)
            self.normal_combobox.setGeometry(10, 440, 91, 41)
            self.normal_combobox.setCurrentIndex(0)
            opacity_effect5 = QGraphicsOpacityEffect() 
            opacity_effect5.setOpacity(0)

            self.admin__maker.setGraphicsEffect(opacity_effect5)
            self.admin__maker.setEnabled(False)
            opacity_effect_inventory_sum = QGraphicsOpacityEffect()
            opacity_effect_inventory_minus = QGraphicsOpacityEffect()
            #percent of opacity
            opacity_effect_inventory_sum.setOpacity(0)
            opacity_effect_inventory_minus.setOpacity(0)

            #seting opacity's 
            self.changing__inventory_sum.setGraphicsEffect(opacity_effect_inventory_sum)
            self.changing__inventory_minus.setGraphicsEffect(opacity_effect_inventory_minus)
            #unablening buttons
            self.changing__inventory_minus.setEnabled(False)
            self.changing__inventory_sum.setEnabled(False)
            #setting Geometry
            self.changing__inventory_minus.setGeometry(370, 450, 141, 28)
            self.changing__inventory_sum.setGeometry(210, 450, 141, 28)
            self.admin__maker.setGeometry(120, 10, 101, 28)  

        elif self.normal_combobox.currentText() == "درباره" or self.admin_combobox.currentText() == "درباره":
            if self.admin_combo:
                c.execute("SELECT * FROM admin_user WHERE user_name = ?", (self.current_user_name,))
                account_info_admin = c.fetchone()

                    
                if account_info_admin:
                        QMessageBox.information(
                            self,
                            "درباره",
                            f"    نام : {account_info_admin[1]} {account_info_admin[2]} \n   نوع اکانت : ادمین\n   کد ملی : {account_info_admin[3]}"     
                        )
                        self.admin_combobox.setCurrentIndex(0) 
            elif self.normal_combo:
                
                    c.execute("SELECT * FROM user WHERE user_name = ?", (self.current_user_name,))
                    account_info_normal = c.fetchone()

                    
                    if account_info_normal:
                        QMessageBox.information(
                            self,
                            "درباره",
                            f"  نام : {account_info_normal[1]} {account_info_normal[2]} \n نوع اکانت : دانش اموز \n  پایه : {account_info_normal[4] } \n  کلاس : {account_info_normal[5]} \n  کد ملی : {account_info_normal[3]}"     
                        )
                        self.normal_combobox.setCurrentIndex(0) 
            elif self.admin_maker_combo == True:
                QMessageBox.information(
                         self,
                         "درباره",
                         f"    نام : mahrad \n   نوع اکانت : سازنده ی اکانت ادمین"     
                    )
                self.admin_combobox.setCurrentIndex(0)

                
                
            

            

        
# GUI show
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    label = QLabel(window)
    app.exec_() 

       
# Close the database connection
conn.close()


