from send import Communication

def main():

    id_to_send = 0
    data_to_send = 100

    assert id_to_send <= 7 and id_to_send >= 0
    assert data_to_send <= 2047 and data_to_send >= 0

    comm = Communication()
    byte0 = (id_to_send << 4) | (data_to_send & 0x0f)
    byte1 = (data_to_send & 0x7f) | 0x80

    comm.send(byte0)
    msg = comm.receive()
    print msg

    comm.send(byte0)
    msg = comm.receive()
    print msg

    comm.close()

if __name__ == '__main__':
    main()
