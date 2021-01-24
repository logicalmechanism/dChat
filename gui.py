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
sg.theme('Black')


# Screen Layout
layout = [
    [sg.Text('Chat: ' + parameters.createChatHash())],
    [sg.Text('Channel: ' + parameters.createChannelHash())],
    [sg.Button("QUIT"), sg.Button("REFRESH")],
    [
        sg.Button("Wallet QR Code"),
        sg.Button("Return ADA", key='-RETURN-'),
        sg.Text("Return ADA", key='-RETURNTEXT-', visible=False),
        sg.Button('Confirm', key='-RCONFIRM-', visible=False),
        sg.Button('Cancel', key='-RCANCEL-', visible=False)
    ],
    [sg.Image(filename='', key='-QRCODE-', visible=False)],
    [sg.Text('Click Refresh',size=(96,48), key='-OUTPUT-', background_color='black')],
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
        window['-OUTPUT-'].update("Sending Message to the Network. Please Click REFRESH")
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
    if event == "-RETURN-":
        window['-RETURNTEXT-'].update(visible=True)
        window['-RCONFIRM-'].update(visible=True)
        window['-RCANCEL-'].update(visible=True)
        window['-RETURN-'].update(visible=False)
    if event == "-RCONFIRM-":
        window['-RCONFIRM-'].update(visible=False)
        window['-RCANCEL-'].update(visible=False)
        window['-RETURNTEXT-'].update(visible=False)
        window['-RETURN-'].update(visible=True)
        function = [
            'bash',
            'return_trx.sh'
        ]
        output = subprocess.check_output(function)
        window['-OUTPUT-'].update("Returning All Funds. Please Click REFRESH.")
        #
    if event == '-RCANCEL-':
        window['-RCONFIRM-'].update(visible=False)
        window['-RCANCEL-'].update(visible=False)
        window['-RETURNTEXT-'].update(visible=False)
        window['-RETURN-'].update(visible=True)



# Close
window.close()