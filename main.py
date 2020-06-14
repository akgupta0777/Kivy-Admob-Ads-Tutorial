from kivmob import KivMob,TestIds,RewardedListenerInterface

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.theming import ThemeManager
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivymd.toast import toast
Builder.load_string(
'''
#.import MDFloatingActionButton kivymd.uix.button.MDFloatingActionButton
#.import MDRaisedButton kivymd.uix.button.MDRaisedButton
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

<Screenmgr>:
    SimpleUI:
    InterstitialAdScreen:
    Rewarded:
    
<SimpleUI>:
    name:"UI"
    Label:
        text: "Banner Ads Are shown at bottom"
        color:[1,1,1,1]
        pos_hint:{"center_x":0.5,"top":1.2}
    MDRaisedButton:
        text:"Interstitial Ad Screen"
        pos_hint:{"center_x":0.5,"top":0.6}
        on_release:
            app.root.transition = SlideTransition(direction = "left")
            app.root.current = "Interstitial"
    
    MDRaisedButton:
        text:"Rewarded Video AD Screen"
        pos_hint:{"center_x":0.5,"top":0.4}
        on_release:
            app.root.transition = SlideTransition(direction = "left")
            app.root.current = "rewarded"
            
<InterstitialAdScreen>:
    name: "Interstitial"
    MDRaisedButton:
        text:"Click To see Interstitial"
        pos_hint:{"center_x":0.5,"top":0.6}
        on_release:
            root.Show()
    
    MDRaisedButton:
        text:"Back"
        pos_hint:{"center_x":0.5,"top":0.8}
        on_release:
            app.root.transition = SlideTransition(direction = "left")
            app.root.current = "UI"

<Rewarded>:
    name: "rewarded"
    MDLabel:
        text:"Points :"+str(app.points)
        halign: "center"
    MDFloatingActionButton:
        icon:"plus"
        elevation_normal:2
        pos_hint:{"center_x":0.5,"center_y":0.30}
        on_release:
            app.ads.show_rewarded_ad()
    MDRaisedButton:
        text:"Leave Screen"
        pos_hint:{"center_x":0.5,"top":0.2}
        on_release:
            app.root.transition = SlideTransition(direction = "left")
            app.root.current = "UI"

'''
)
class Screenmgr(ScreenManager):
    pass

class SimpleUI(Screen):
    pass

class InterstitialAdScreen(Screen):
    def on_pre_enter(self, *args):
        SimpleApp.ads.request_interstitial()    # Intersitial ads is loaded in memory

    def on_pre_leave(self, *args):
        SimpleApp.ads.request_interstitial()  # reloading ad again .

    def Show(self):
        SimpleApp.ads.show_interstitial()

class Rewarded(Screen):
    pass


class SimpleApp(MDApp):
    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        super().__init__(**kwargs)
        self.rewards = Rewards_Handler(self)

    ads = KivMob(TestIds.APP) # put your Admob Id in case you want to put your own ads.
    points = NumericProperty(0)
    def build(self):
        self.ads.new_banner(TestIds.BANNER,False)
        self.ads.request_banner()
        self.ads.show_banner()
        self.ads.new_interstitial(TestIds.INTERSTITIAL)
        self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
        self.ads.set_rewarded_ad_listener(self.rewards)

        return Screenmgr()

    def load_video(self):
        self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)


class Rewards_Handler(RewardedListenerInterface):
    def __init__(self,other):
        self.AppObj = other


    def on_rewarded(self, reward_name, reward_amount):
        self.AppObj.points += int(reward_amount)   # in Sample ad unit default amount is 10
        toast("User recieved 10 points")

    def on_rewarded_video_ad_started(self):    # Reloading Ad
        self.AppObj.load_video()

    def on_rewarded_video_ad_completed(self):
        self.on_rewarded("Points","10")

    def on_rewarded_video_ad_closed(self):
        self.AppObj.points += 0

if __name__ == "__main__":
    SimpleApp().run()

