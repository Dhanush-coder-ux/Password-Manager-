import flet as ft
from password import encrypt,decrypt,delet
import random
import string
import os


def main(page: ft.Page):
    page.theme_mode="dark"
    a=ft.Ref[ft.TextField]()
    b=ft.Ref[ft.TextField]()
    r=ft.Ref[ft.Text]()
    c=ft.Ref[ft.TextField]()
    pcall=ft.Ref[ft.Column]()
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.bgcolor="#232F34"
    def back(e):
        page.views.pop()
        page.update()

    def copy(e):
        page.set_clipboard(e.control.key)
        page.update()
    def create(e):
        
        if e.control.data=='create':

            page.views.append(createpassword())
            page.update()
        elif  e.control.data=='generate':
            page.views.append(generatepassword())
            page.update()
        elif e.control.data=='random':
            random_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=10))
            r.current.value=random_password
            page.update()
        elif e.control.data=='info':
            page.views.append(infopage())
            page.update()        
        elif e.control.data=='encrypt':
            encrypt(a.current.value,b.current.value,None)
            a.current.value = ""
            b.current.value = ""
            page.update()
            if not a.current.value and b.current.value :
                page.snack_bar=ft.SnackBar(ft.Text(value=" Oops !! Value Not Found !",color=ft.Colors.ORANGE_300),bgcolor=ft.colors.WHITE)
                page.snack_bar.open=True
                page.update()
            else:
                page.snack_bar=ft.SnackBar(ft.Text(value=" Successfully Created Your Domain And Password!",color=ft.Colors.ORANGE_300),bgcolor=ft.colors.WHITE)
                page.snack_bar.open=True
                page.update()

        elif e.control.data == 'click':

            current_password = c.current.value   
            
            if os.path.exists('mainpassword.txt'):
                with open('mainpassword.txt', 'r') as ma:
                    saved_password = ma.read()
            else:
                with open('mainpassword.txt', 'w') as main:
                    main.write(current_password)
                saved_password=current_password
            
            def delete(e):
                
                delet(e.control.data['domain'],e.control.data['domain_password'])
                pcall.current.controls.pop(int(e.control.key))
                
                page.update()

            if current_password == saved_password:  
                page.views.append(seepassword())  
                page.update()
                decryptpasswords=decrypt()
                pcall.current.controls.extend(
                    [
                        ft.ExpansionPanelList(
                            expand_icon_color=ft.Colors.WHITE,
                            controls=[
                                
                                ft.ExpansionPanel(can_tap_header=True,bgcolor=ft.Colors.PURPLE_300,
                                
                                    header=ft.Row([ft.Text(decryptpasswords['domain'][i],weight=ft.FontWeight.W_500,size=25),
                                                   ft.IconButton(ft.icons.DELETE,data={'domain':decryptpasswords['domain'][i],'domain_password':decryptpasswords['domain_password'][i]},on_click=delete,key=str(i)),],
                                                   alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                    content=ft.Row([ft.Text(decryptpasswords['domain_password'][i],weight=ft.FontWeight.W_400,size=20,color=ft.Colors.GREY_50),
                                                    ft.IconButton(ft.icons.COPY,key=decryptpasswords['domain_password'][i],on_click=copy),
                                                   ],
                                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY),expand=True
                                    
                                )
                                for i in range (len(decryptpasswords['domain']))
                            ]
                        )
                    ]
                    
                )
                page.update()
            else:
                page.snack_bar=ft.SnackBar(ft.Text(value="Incorrect Password",color=ft.Colors.GREY_500),bgcolor=ft.colors.BLACK38,padding=20)
                page.snack_bar.open=True
                page.update()

        elif e.control.data == 'forget':

            if os.path.exists('mainpassword.txt'):
                os.remove('mainpassword.txt')
                page.snack_bar=ft.SnackBar(ft.Text(value="Password was Removed Now Create A New Password !",color=ft.Colors.BLUE_400),bgcolor=ft.colors.BLACK38,padding=20)
                page.snack_bar.open=True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Password Does not exists"))  
                page.snack_bar.open = True
                page.update()
        

    def mainpass(e):
         page.open(
            ft.BottomSheet(bgcolor=ft.Colors.with_opacity(0.10, ft.Colors.WHITE),
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.TextField(label="Enter Your Master Password",
                                            label_style=ft.TextStyle(color=ft.Colors.WHITE),
                                            border_color=ft.Colors.WHITE,
                                            border_radius=30,
                                            password=True,
                                            can_reveal_password=True,
                                            ref=c
                                            ),
                                ft.ElevatedButton(text="Check",width=150,height=50,bgcolor=ft.Colors.TRANSPARENT,color="white",data='click',on_click=create),
                                ft.TextButton("Foget Passwword",data="forget",on_click=create)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=30
                        ),
                        height=250,
                        padding=10,
                        border_radius=50,
                        
                    ),
            )
     )
    def seepassword():
        return ft.View(bgcolor="white",scroll=ft.ScrollMode.ALWAYS,
            appbar=ft.AppBar(
                leading=ft.IconButton(ft.Icons.ARROW_BACK,icon_color=ft.colors.PURPLE_300,on_click=back),
                leading_width=40,
                toolbar_height=80,
                title=ft.Text("YOUR PASSWORD",color=ft.Colors.WHITE70,weight=ft.FontWeight.W_500),
                bgcolor=ft.Colors.PURPLE_600,    
            ),
            controls=[
             ft.Column(
                 ref=pcall
             )
            ]
            
        ) 


    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.LOCK),
        leading_width=40,
        toolbar_height=80,
        
        title=ft.Text("PASSWORD ",color=ft.Colors.WHITE70,weight=ft.FontWeight.W_500,text_align="center"),
        bgcolor=ft.Colors.BLACK,
        actions=[
            ft.IconButton(ft.Icons.REMOVE_RED_EYE,icon_color=ft.Colors.WHITE,on_click=mainpass),
            ft.IconButton(ft.Icons.INFO_OUTLINE_ROUNDED,data='info',on_click=create),
         
        ],
    )
    
    
    def createpassword():
        
        return ft.View(bgcolor="#FFFBE6",
            
            appbar= ft.AppBar(
                    leading=ft.IconButton(ft.Icons.ARROW_BACK,icon_color=ft.Colors.ORANGE_300,on_click=back),
                    leading_width=40,
                    toolbar_height=80,
                    
                    title=ft.Text("STORE P@SSW0RD",color=ft.Colors.ORANGE_400,weight=ft.FontWeight.W_500),
                    bgcolor=ft.Colors.WHITE,
           
                  ) 
            ,controls=[
        
        ft.Container(
            
            #blur=ft.Blur(sigma_x=300, sigma_y=300), 
            
            width=400,
            height=400,
            alignment=ft.Alignment(0, 0),
            border_radius=30,
            padding=30,
            shadow=ft.BoxShadow(0,10,color="grey",blur_style=ft.ShadowBlurStyle.OUTER),
            #bgcolor=ft.Colors.with_opacity(0.10, ft.Colors.WHITE),
            bgcolor=ft.Colors.WHITE54, 
            content=ft.Column(
                [
                  
                    ft.Row([ft.Text(value="STORE PASSWORD",weight=ft.FontWeight.W_900,color=ft.Colors.ORANGE_400,size=20),ft.Icon(ft.Icons.LOCK,color=ft.Colors.ORANGE_400)]),
                    ft.Divider(height=10,color=ft.colors.ORANGE_400),
                   ft.TextField(
                        label="Enter Domain Name !!",
                        border_radius=30,
                        border_color=ft.Colors.ORANGE_400,
                        width=300, 
                        ref=a,
                        color=ft.colors.BLACK38,
                        label_style=ft.TextStyle(color=ft.colors.ORANGE_400),
                        
                        
                    ),
                   
                   
                    ft.TextField(
                       ref=b,
                        label="Enter Domain Password !!",
                        border_radius=30,
                        border_color=ft.Colors.ORANGE_400,
                        width=300, 
                       
                        can_reveal_password=True,
                        password=True,
                        color=ft.colors.BLACK38 ,
                        label_style=ft.TextStyle(color=ft.colors.ORANGE_400),
                       
                    ),
                    ft.Divider(height=10,color=ft.colors.ORANGE_400),
                    ft.ElevatedButton(
                        text="STORE",
                        data='encrypt',
                        color=ft.colors.ORANGE_400,
                        width=300,
                        height=40,
                        bgcolor=ft.Colors.WHITE,
                        on_click=create, 
                        
                    ),
                ],
                spacing=20,  
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER
                
            )

        
    def generatepassword():
        return ft.View(bgcolor=ft.colors.WHITE,
                appbar= ft.AppBar(
                    leading=ft.IconButton(ft.Icons.ARROW_BACK,on_click=back,icon_color="#37966F"),
                    leading_width=40,
                    toolbar_height=80,
                        
                    title=ft.Text("GENERATE P@SSW0RD",color=ft.Colors.WHITE70,weight=ft.FontWeight.W_500),
                    bgcolor="#356859"
                   
                    ),controls=[
                        ft.Container(
                        #blur=ft.Blur(sigma_x=100,sigma_y=100),
                        height=300,
                        width=350,
                        alignment=ft.Alignment(0, 0),
                        border_radius=30,
                         shadow=ft.BoxShadow(0,4,color="grey",blur_style=ft.ShadowBlurStyle.OUTER),
                    padding=30,
                        bgcolor="#B9E4C9",
                       content=ft.Column(
                                [
                                    ft.Text(value="Generatepassword",color="#37966F",weight=ft.FontWeight.W_500,size=30,ref=r),
                                    ft.IconButton(ft.Icons.EDIT,icon_size=30,icon_color="#37966F",data='random',on_click=create)
                                ],spacing=20,  
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        )
                        
                    ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )   
    
    def infopage():
        return  ft.View(bgcolor="#FFFBE6",
                        scroll=ft.ScrollMode.ALWAYS,
            appbar=ft.AppBar(
                leading=ft.IconButton(ft.Icons.ARROW_BACK,on_click=back,icon_color="#B9E4C9"),
                leading_width=40,
                toolbar_height=80,
                title=ft.Text("INFORMATION", color=ft.Colors.WHITE70,weight=ft.FontWeight.W_500),
                bgcolor="#37966F",
            ),
        controls=[
               ft.Column([ft.Text(value="Password Manager",color="#356859",size=30,weight=ft.FontWeight.W_400)]),
        ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    bgcolor="#B9E4C9",
                    header=ft.Text('INTRODUCTION',color="black",text_align="center",weight=ft.FontWeight.W_500,size=15),
                    content=ft.Text(color="grey",value='A password manager application designed to securely store, manage, and retrieve user credentials !!',weight=ft.FontWeight.W_400,size=15),can_tap_header=True
                )
            ]
        ),
        ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    bgcolor="#B9E4C9",
                    header=ft.Text(color="black",value="Encryption and Decryption",weight=ft.FontWeight.W_500,size=15,text_align="center"),
                    content=ft.Text(color="grey",text_align="center",value="Decryption occurs only when authorized by the user through a master password  end-to-end encryption, meaning no plain-text data is ever exposed, even during syncing across devices",weight=ft.FontWeight.W_400,size=15),can_tap_header=True
                )
            ]
        ),
           ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    bgcolor="#B9E4C9",
                    header=ft.Text(text_align="center",color="black",value="Advantages and Storage",weight=ft.FontWeight.W_500,size=15),
                    content=ft.Text(color="grey",text_align="center",value="Your Domain Name And Passwords After Encryption, It Create An File On Your Device And Stores That Encrypted Data Into That File.It Can't Store Your Data Into Any Servers Or DataBase. So, It Gives Additional Security Feature For Your Data And This Is An Advantage Of This Password Manager Application. ",size=15,weight=ft.FontWeight.W_400),can_tap_header=True
                )
            ]
        ),
           ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    
                    bgcolor="#B9E4C9",
                    
                    header=ft.Text(text_align="center",color="black",value="Attention",weight=ft.FontWeight.W_500,size=15),
                    content=ft.Text(color="grey",text_align="center",value="Before Uninstall Or Changing Mobile, Make Sure You Recoverd Your Domain Name And Passwords. Otherwise Recover It. Because It Stores Your Domain Name and Passwords On Your Device Only.",weight=ft.FontWeight.W_400,size=15),can_tap_header=True
                )
            ]
        ),
        ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    bgcolor="#B9E4C9",
                    header=ft.Text(text_align="center",color="black",value="About Version",weight=ft.FontWeight.W_500,size=15),
                    content=ft.Text(color="grey",text_align="center",value="The Current Version of PasswordManager Is v2.0",weight=ft.FontWeight.W_400,size=15),can_tap_header=True
                )
            ]
        )
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
        )
    page.add(
            
            
                ft.Container(
                    blur=ft.Blur(sigma_x=100,sigma_y=100),
                    bgcolor=ft.Colors.with_opacity(0.10, ft.Colors.WHITE), 
                    
                    width=400,
                    
                    alignment=ft.Alignment(0,0),
                    border_radius=40,
                    padding=30,
                   #shadow=ft.BoxShadow(0,10,color="grey",blur_style=ft.ShadowBlurStyle.OUTER),
                    
                    content=ft.Column(
                        [
                            ft.ElevatedButton(
                                text="STORE PASSWORD",
                                color=ft.Colors.WHITE,
                               width=400,
                               height=80, 
                               bgcolor=ft.Colors.TRANSPARENT,
                               data='create',
                               on_click=create
                               
                            
                            ),
                            ft.ElevatedButton(
                                text="GENERATE PASSWORD",
                                color=ft.Colors.WHITE,
                                 width=400,
                               height=80,
                               bgcolor=ft.Colors.TRANSPARENT,
                               data='generate',
                               on_click=create
                             
                            ),
                        ],
                
                        
                         
                    ),
                ),
        )
   
    page.on_view_pop = back
    
    


ft.app(target=main)