import src.scrapMetaData as scrapMetaData
import src.parameters as parameters
import src.functions as functions
import subprocess
import PySimpleGUI as sg
import random

# Wallet Addr
wallet_addr = ''
with open('main_user/main_base.addr', 'r') as file:
    wallet_addr = file.read()[:-1]
sg.theme('DarkAmber')

# Header
header = [
    sg.Text('Chat: ' + parameters.createChatHash()),
    sg.Text('Channel: ' + parameters.createChannelHash()),
    sg.Button('QR Code'),
    sg.Button("QUIT")
]

# Body
body = [sg.Text('Click Refresh',size=(128,48), key='-OUTPUT-', background_color='black')]

# Screen Layout
layout = [
    [sg.Text('Chat: ' + parameters.createChatHash())],
    [sg.Text('Channel: ' + parameters.createChannelHash())],
    [sg.Button("QUIT"), sg.Button("REFRESH")],
    [sg.Button("Wallet QR Code"), sg.Button("Return ADA")],
    [sg.Image(filename='', key='-QRCODE-', visible=False)],
    body,
    [
        sg.Text("Username:"),
        sg.Input(key='-USER-', size=(16,1)),
        sg.Text("Lovelace:"),
        sg.Text("", key='-ADA-', size=(10,1)),
        sg.Text("Fee:"),
        sg.Text("", key='-FEE-', size=(10,1)),
        sg.Text("Change:"),
        sg.Text("", key='-CHANGE-', size=(10,1)),
    ],
    [
        sg.Multiline(key='-IN-', size=(64,12)),
        sg.Button('Send', key='-SEND-', visible=True),
        sg.Button('Confirm', key='-CONFIRM-', visible=False),
        sg.Button('Cancel', key='-CANCEL-', visible=False),
    ]
]

# Create the window
window = sg.Window("dChat", layout)

# Create an event loop
while True:
    event, values = window.read(timeout=10000)
    
    # QUIT button
    if event == "QUIT" or event == sg.WIN_CLOSED:
        break

    # QR Code
    if event == "Wallet QR Code":
        if window['-QRCODE-'].visible is True:
            window['-QRCODE-'].hide_row()
            window['-QRCODE-'].update(filename='', visible=False)
        else:
            window['-QRCODE-'].unhide_row()
            window['-QRCODE-'].update(filename='./main_user/main_qrcode.png',visible=True)

    # Send a new message
    if event == "-SEND-":

        # Username and message
        username, message = parameters.formatData(values)
        if message != '':
            parameters.create(username, message)
            function = [
                'bash',
                'self_trx_fee.sh'
            ]
            output = subprocess.check_output(function)
            balance = functions.getBalance(wallet_addr)
            window['-CONFIRM-'].update(visible=True)
            window['-CANCEL-'].update(visible=True)
            window['-SEND-'].update(visible=False)
            change = balance - int(output.decode('utf-8'))
            window['-CHANGE-'].update(change)
            window['-FEE-'].update(str(output.decode('utf-8')))
    
    # Confirm button
    if event == "-CONFIRM-":
        function = [
            'bash',
            'self_trx_submit.sh'
        ]
        output = subprocess.check_output(function)
        window['-SEND-'].update(visible=True)
        window['-CONFIRM-'].update(visible=False)
        window['-CANCEL-'].update(visible=False)
        window['-IN-'].update('')
        window['-FEE-'].update('')
        window['-CHANGE-'].update('')
    
    # Cancel Button
    if event == "-CANCEL-":
        window['-SEND-'].update(visible=True)
        window['-CONFIRM-'].update(visible=False)
        window['-CANCEL-'].update(visible=False)
        window['-IN-'].update('')
        window['-FEE-'].update('')
        window['-CHANGE-'].update('')

    # Update the chat window
    if event == "REFRESH":
        balance = functions.getBalance(wallet_addr)
        window['-ADA-'].update(balance)
        window['-OUTPUT-'].update("Loading Chat Messages...")
        data = scrapMetaData.get_last_transaction()
        text = ""
        for message in data:
            for msg in message:
                if int(msg) == 3:
                    text += '\n' + message[msg] +'\n'
                if int(msg) > 3:
                    text += message[msg] +'\n'
        window['-OUTPUT-'].update(text)
    
    # Return All ADA to return address
    if event == "Return ADA":
        function = [
            'bash',
            'return_trx.sh'
        ]
        output = subprocess.check_output(function)
# Close
window.close()