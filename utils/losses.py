from cmath import log, log10, pi, sqrt

def loss_hata_medium(freq, h_gw, h_en, distanza):
    loss = 0

    # OKOMURA_hata_medium per piccole/medie città
    C_h = 0.8 + (1.1*log10(freq)-0.7)*h_en - 1.56*log10(freq)

    loss = 69.55 + 26.16*log10(freq) - 13.82*log(h_gw) - \
        C_h + (44.9 - 6.55*log10(h_gw))*log10(distanza)

    return loss

def loss_hata_big(freq, h_gw, h_en, distanza):
    loss = 0

    # OKOMURA_hata_medium per piccole/medie città

    a_h_en = 3.2*( log10(11.54*h_en))**2 - 4.97
    A = 69.55 + 26.16*log10(freq) - 13.82*log10(h_gw)
    B = 44.9 - 6.55*log10(h_gw)
    loss = A - a_h_en + B*log10(distanza)

    return loss

def loss_SUI_medium(freq, h_gw, h_en, distanza):
    # reference distance for SUI model is d_0 = 100
    A = 20*log10(4*pi*100/(3*10**8/(freq*10**6))) # does represent the free space losso at reference distance d_0 = 100

    ## parameters tied to terrain
    #       Terr A  Terr B  Terr C
    #   a   4.6     4       3.6
    #   b   0.0075  0.0065  0.005
    #   c   12.6    17.1    20
    ## whre A-> big city | B-> medium city | C-> vegetation

    a = 4
    b = 0.0065
    c = 17.1

    ## X_f = 6*log10(freq/2000) se la freq supera i 2GHz
    X_f=0

    ## per Terr A e B
    X_h = -10.8*log10(h_en/2000)
    # per Terr C da -10.8 a 20
    s = 0 # fattore correzione dello shadowing

    gamma = a - b*h_gw + c/h_gw
    loss = ( A + 10*gamma*log10(distanza*1000/100) + X_f + X_h + s )

    loss = abs(loss)

    return loss

def loss_SUI_big(freq, h_gw, h_en, distanza):
    # reference distance for SUI model is d_0 = 100
    A = 20*log10(4*pi*100/(3*10**8/(freq*10**6))) # does represent the free space losso at reference distance d_0 = 100

    ## parameters tied to terrain
    #       Terr A  Terr B  Terr C
    #   a   4.6     4       3.6
    #   b   0.0075  0.0065  0.005
    #   c   12.6    17.1    20
    ## whre A-> big city | B-> medium city | C-> vegetation

    a = 4.6
    b = 0.0075
    c = 12.6

    X_f = 6*log10(freq/2000)

    ## per Terr A e B da 20 a 10.8
    X_h = -20*log10(h_en/2000)
    # per Terr C da 10.8 a 20
    s = 0 # fattore correzione dello shadowing

    gamma = a - b*h_gw + c/h_gw
    loss = abs( A + 10*gamma*log10(distanza*1000/100) + X_f + X_h + s )

    return loss

def loss_ericsson(freq, h_gw, h_en, distanza):

    a_0 = 36.2
    a_1 = 30.2
    a_2 = 12.0
    a_3 = 0.1

    g_f = 44.49*log10(freq) - 4.78*(log10(freq))**2

    loss = a_0 + a_1*log10(distanza) + a_2*log10(h_gw) + a_2*log10(h_gw)*log10(distanza) - 3.2*(log10(11.75*h_en))**2 +g_f
    return loss

def loss_ericsson_medium(freq, h_gw, h_en, distanza):

    a_0 = 43.2
    a_1 = 68.93
    a_2 = 12.0
    a_3 = 0.1

    g_f = 44.49*log10(freq) - 4.78*(log10(freq))**2

    loss = a_0 + a_1*log10(distanza) + a_2*log10(h_gw) + a_2*log10(h_gw)*log10(distanza) - 3.2*(log10(11.75*h_en))**2 +g_f
    return loss