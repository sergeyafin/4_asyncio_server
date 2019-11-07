import asyncio


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    name=''
    check=False
    names = open('names.txt','r')
    nameflag=0#user is unknown
    for i in names:#check ip in names.txt
        
        if i.split(',')[0][2:-1]==addr[0]:#if ip is known
            nameflag=1#user is known
            
            writer.write('Hello, {0}. Enter password'.format(i.split(',')[1][2:-1]).encode())
            await writer.drain()
            
            name=i.split(',')[1][2:-1]
            while check!=True:
                psw = await reader.read(100)
                if i.split(',')[2][2:-3]==(str(psw)[2:-1]):
                    writer.write('''Password is right
Type "gl_msg" to send message to global chat.
Type "show_gl" to show global chat
Type "exit" to exit
Type another message for echo chat'''.encode())
                    await writer.drain()
                    check=True
                    
                if check==False:
                    writer.write('Password is wrong! Try again'.encode())
                    await writer.drain()
                
    names.close()
    if nameflag==0:
        writer.write(r"Hello, stranger! What's your name?".encode())
        await writer.drain()
        name = await reader.read(100)
        writer.write("Hello, {0}! Create password!".format(str(name)[2:]).encode())
        await writer.drain()
        psw = await reader.read(100)
        names = open('names.txt','a')
        names.write(str([addr[0],str(name.decode()),str(psw)[2:-1]])+"\n")
        writer.write('''Welcome to my server!
Type "gl_msg" to send message to global chat.
Type "show_gl" to show global chat
Type "exit" to exit
Type another message for echo chat'''.encode())
        await writer.drain()
        names.close()
        check=True
    
        
        
    while check==True:
        
        data = await reader.read(100)
        message = data.decode()
        
        
        if message == 'exit':
            writer.close()
            print(f'OH NO! WE LOST {name} !!!')

        if message =='gl_msg':
            writer.write("Enter your global message".encode())
            await writer.drain()
            gl_msg = await reader.read(100)
            gl_chat = open('gl_chat.txt','a')
            gl_chat.write(str(name)+'>>>'+gl_msg.decode()+'\n')
            gl_chat.close()
            chat=[]
            gl_chat = open('gl_chat.txt','r')
            for i in gl_chat:
                chat.append(i)
            st_chat='\n'.join(chat)
            writer.write(st_chat.encode())
            await writer.drain()
            gl_chat.close()
        elif message =='show_gl':
            chat=[]
            gl_chat = open('gl_chat.txt','r')
            for i in gl_chat:
                chat.append(i)
            st_chat='\n'.join(chat)
            writer.write(st_chat.encode())
            await writer.drain()
            gl_chat.close()
        else:    
            print(f'{name} said: {message!r}') 
            message_new = f'You said {message!r}'
            writer.write(message_new.encode())
            await writer.drain()
        


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 9095)
    users=[]
    ser = server.sockets[0].getsockname()
    print(f'Serving on {ser}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
