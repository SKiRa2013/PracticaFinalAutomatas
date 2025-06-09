from finitestate_automata.lexical import *

from pushdown_automata.terminal import *
from pushdown_automata.non_terminal import *
from pushdown_automata.action import *

from kiratools.stack import *
from kiratools.conversion_expr import *

import os

class Practica2:
    def __init__(self, lex: Lexical):
        self.automata = Stack("Pila de Autómata")
        self.input_tape = lex.string_tape
  
        self.execute_analysis()
        
        empty_stack = self.automata.is_empty()
        empty_tape = self.input_tape.is_empty()
        
        print(f"\n{"="*90}")
        print(f"\nPila: ▼ {"" if self.automata.is_empty() else "," } {self.automata}\nCinta: {self.input_tape}{"" if self.input_tape.is_empty() else ","} ⊣\n")
        
        if not empty_stack and empty_tape:
            print("Elementos residuales en pila, pero no se ha llegado al fin de secuencia. RECHACE LA SECUENCIA.")
            return
        
        if empty_stack and not empty_tape:
            print("Pila vacía pero hay elementos extra en la cinta de entrada. RECHACE LA SECUENCIA.")
        
        if empty_stack and empty_tape:
            print("Fin de secuencia y pila vacía. ACEPTE LA SECUENCIA.")
            return
        
        print("Error desconocido. RECHACE.")
    
    def infija_a_prefija(self, string: str) -> str:
        return ConversionExpr(string).prefija
    
    def infija_a_posfija(self, string: str) -> str:
        return ConversionExpr(string).posfija
    
    def arreglar_infija(self, string: str) -> str:
        return ConversionExpr(string).infija
        
    def axiom(self):
        s = NoTerminal("S")
        
        self.automata.push_node(s)   
    
    def operation_S(self):
        sv1_e = Sintetized("sv1")
        sv2_e = Sintetized("sv2")
        
        iv1_resp = Inherited("iv1")
        iv2_resp = Inherited("iv2")
        
        e_sv1_sv2 = NoTerminal("E")
        e_sv1_sv2.sintetized.append(sv1_e)
        e_sv1_sv2.sintetized.append(sv2_e)
        
        resp = Action("Respuesta")
        resp.inherited.append(iv1_resp)
        resp.inherited.append(iv2_resp)
        
        iv1_resp.ref = sv1_e                                                    # iv1 <- sv1
        sv1_e.attr_users.append(iv1_resp)
        
        iv2_resp.ref = sv2_e                                                    # iv2 <- sv2
        sv2_e.attr_users.append(iv2_resp)
        
        resp.add_exec(lambda iv1, iv2, _: 
                          print(f"Respuesta: {iv1.value}\nPrefija: {self.infija_a_prefija(iv2.value)}\nInfija: {self.arreglar_infija(iv2.value)}\nPosfija: {self.infija_a_posfija(iv2.value)}"), 
                      iv1_resp, iv2_resp, snt_dest=None)
        
        self.automata.push_node(resp)
        self.automata.push_node(e_sv1_sv2)
        
    def operation_E(self):        
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "E":
            raise ValueError("Unexpected top node in machine stack")
        
        sa1_t = Sintetized("sa1")
        sa2_t = Sintetized("sa2")
        
        i1_el = Inherited("i1")
        i2_el = Inherited("i2")
        
        s1_el = Sintetized("s1")
        s2_el = Sintetized("s2")
        
        t_sa1_sa2 = NoTerminal("T")
        t_sa1_sa2.sintetized.append(sa1_t)
        t_sa1_sa2.sintetized.append(sa2_t)
        
        el_i1_i2_s1_s2 = NoTerminal("E_L")
        el_i1_i2_s1_s2.inherited.append(i1_el)
        el_i1_i2_s1_s2.inherited.append(i2_el)
        el_i1_i2_s1_s2.sintetized.append(s1_el)
        el_i1_i2_s1_s2.sintetized.append(s2_el)
        
        i1_el.ref = sa1_t                                                       # i1 <- sa1
        sa1_t.attr_users.append(i1_el)
        
        i2_el.ref = sa2_t                                                       # i2 <- sa2
        sa2_t.attr_users.append(i2_el)
        
        s1_el.attr_users.append(tope_pila.sintetized[0])                        # sv1 <- s1: Se deja pendiente para propagación de valores
        s2_el.attr_users.append(tope_pila.sintetized[1])                        # sv2 <- s2: Se deja pendiente para propagación de valores 
              
        self.automata.push_node(el_i1_i2_s1_s2)
        self.automata.push_node(t_sa1_sa2)
        
    def operation_E_L1(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "E_L":
            raise ValueError("Unexpected top node in machine stack")
        
        sa1_t = Sintetized("sa1")
        sa2_t = Sintetized("sa2")
        
        isa_suma = Inherited("isa")
        isb_suma = Inherited("isb")
        isc_suma = Inherited("isc")
        isd_suma = Inherited("isd")
        
        ss_suma = Sintetized("ss")
        ses_suma = Sintetized("ses")
        
        i3_el = Inherited("i3")
        i4_el = Inherited("i4")
        
        s3_el = Sintetized("s3")
        s4_el = Sintetized("s4")
        
        term_plus = Terminal("symbol", "+")
        
        t_sa1_sa2 = NoTerminal("T")
        t_sa1_sa2.sintetized.append(sa1_t)
        t_sa1_sa2.sintetized.append(sa2_t)
        
        suma = Action("Suma")
        suma.inherited.append(isa_suma)
        suma.inherited.append(isb_suma)
        suma.inherited.append(isc_suma)
        suma.inherited.append(isd_suma)
        suma.sintetized.append(ss_suma)
        suma.sintetized.append(ses_suma) 
        
        el_i3_i4_s3_s4 = NoTerminal("E_L")
        el_i3_i4_s3_s4.inherited.append(i3_el)
        el_i3_i4_s3_s4.inherited.append(i4_el)
        el_i3_i4_s3_s4.sintetized.append(s3_el)
        el_i3_i4_s3_s4.sintetized.append(s4_el)
        
        isa_suma.value = tope_pila.inherited[0].value                           # isa <- i1
        isb_suma.ref = sa1_t                                                    # isb <- sa1
        sa1_t.attr_users.append(isb_suma)
        isc_suma.value = tope_pila.inherited[1].value                           # isc <- i2
        isd_suma.ref = sa2_t                                                    # isd <- sa2
        sa2_t.attr_users.append(isd_suma)
        
        suma.add_exec(lambda isa, isb, ss: setattr(ss, "ref", Terminal("ss", isa.value + isb.value)), isa_suma, isb_suma, snt_dest=ss_suma)
        suma.add_exec(lambda isc, isd, ses: setattr(ses, "ref", Terminal("ses", f"{isc.value}+{isd.value}")), isc_suma, isd_suma, snt_dest=ses_suma)         
      
        i3_el.ref = ss_suma                                                     # i3 <- ss
        ss_suma.attr_users.append(i3_el)
        
        i4_el.ref = ses_suma                                                    # i4 <- ses
        ses_suma.attr_users.append(i4_el)
        
        s3_el.attr_users.append(tope_pila.sintetized[0])                        # s1 <- s3: Se deja pendiente para propagación de valores
        s4_el.attr_users.append(tope_pila.sintetized[1])                        # s2 <- s4: Se deja pendiente para propagación de valores
        
        self.automata.push_node(el_i3_i4_s3_s4)
        self.automata.push_node(suma)
        self.automata.push_node(t_sa1_sa2)
        self.automata.push_node(term_plus)
        
    def operation_E_L2(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "E_L":
            raise ValueError("Unexpected top node in machine stack")
        
        sa1_t = Sintetized("sa1")
        sa2_t = Sintetized("sa2")
        
        ira_resta = Inherited("isa")
        irb_resta = Inherited("isb")
        irc_resta = Inherited("isc")
        ird_resta = Inherited("isd")
        
        sr_resta = Sintetized("ss")
        ser_resta = Sintetized("ses")
        
        i3_el = Inherited("i3")
        i4_el = Inherited("i4")
        
        s3_el = Sintetized("s3")
        s4_el = Sintetized("s4")
        
        term_minus = Terminal("symbol", "-")
        
        t_sa1_sa2 = NoTerminal("T")
        t_sa1_sa2.sintetized.append(sa1_t)
        t_sa1_sa2.sintetized.append(sa2_t)
        
        resta = Action("Resta")
        resta.inherited.append(ira_resta)
        resta.inherited.append(irb_resta)
        resta.inherited.append(irc_resta)
        resta.inherited.append(ird_resta)
        resta.sintetized.append(sr_resta)
        resta.sintetized.append(ser_resta) 
        
        el_i3_i4_s3_s4 = NoTerminal("E_L")
        el_i3_i4_s3_s4.inherited.append(i3_el)
        el_i3_i4_s3_s4.inherited.append(i4_el)
        el_i3_i4_s3_s4.sintetized.append(s3_el)
        el_i3_i4_s3_s4.sintetized.append(s4_el)
        
        ira_resta.value = tope_pila.inherited[0].value                          # ira <- i1
        irb_resta.ref = sa1_t                                                   # irb <- sa1
        sa1_t.attr_users.append(irb_resta)
        irc_resta.value = tope_pila.inherited[1].value                          # irc <- i2
        ird_resta.ref = sa2_t                                                   # ird <- sa2
        sa2_t.attr_users.append(ird_resta)
        
        resta.add_exec(lambda ira, irb, sr: setattr(sr, "ref", Terminal("sr", ira.value - irb.value)), ira_resta, irb_resta, snt_dest=sr_resta)
        resta.add_exec(lambda irc, ird, ser: setattr(ser, "ref", Terminal("ser", f"{irc.value}-{ird.value}")), irc_resta, ird_resta, snt_dest=ser_resta)         
      
        i3_el.ref = sr_resta                                                    # i3 <- sr
        sr_resta.attr_users.append(i3_el)
        i4_el.ref = ser_resta                                                   # i4 <- ser
        ser_resta.attr_users.append(i4_el)
        
        s3_el.attr_users.append(tope_pila.sintetized[0])                        # s1 <- s3: Se deja pendiente para propagación de valores 
        s4_el.attr_users.append(tope_pila.sintetized[1])                        # s2 <- s4: Se deja pendiente para propagación de valores
        
        self.automata.push_node(el_i3_i4_s3_s4)
        self.automata.push_node(resta)
        self.automata.push_node(t_sa1_sa2)
        self.automata.push_node(term_minus)    
    
    def operation_E_L3(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "E_L":
            raise ValueError("Unexpected top node in machine stack")
        
        tope_pila.sintetized[0].ref = tope_pila.inherited[0]                    # s3 <- i3
        tope_pila.inherited[0].attr_users.append(tope_pila.sintetized[0])
        
        tope_pila.sintetized[1].ref = tope_pila.inherited[1]                    # s4 <- i4
        tope_pila.inherited[1].attr_users.append(tope_pila.sintetized[1])
        
        self.automata.push_node(Terminal("special", "$"))                       # Hay que apilar el vacío (XD)
        
    def operation_T(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "T":
            raise ValueError("Unexpected top node in machine stack")
        
        sb1_p = Sintetized("sb1")
        sb2_p = Sintetized("sb2")
        
        i5_tl = Inherited("i5")
        i6_tl = Inherited("i6")
        
        s5_tl = Sintetized("s5")
        s6_tl = Sintetized("s6")
        
        p_sb1_sb2 = NoTerminal("P")
        p_sb1_sb2.sintetized.append(sb1_p)
        p_sb1_sb2.sintetized.append(sb2_p)
        
        tl_i5_i6_s5_s6 = NoTerminal("T_L")
        tl_i5_i6_s5_s6.inherited.append(i5_tl)
        tl_i5_i6_s5_s6.inherited.append(i6_tl)
        tl_i5_i6_s5_s6.sintetized.append(s5_tl)
        tl_i5_i6_s5_s6.sintetized.append(s6_tl)
        
        i5_tl.ref = sb1_p                                                       # i5 <- sb1
        sb1_p.attr_users.append(i5_tl)
        i6_tl.ref = sb2_p                                                       # i6 <- sb2
        sb2_p.attr_users.append(i6_tl)
        s5_tl.attr_users.append(tope_pila.sintetized[0])                        # sa1 <- s5: Se deja pendiente para propagación de valores
        s6_tl.attr_users.append(tope_pila.sintetized[1])                        # sa2 <- s6: Se deja pendiente para propagación de valores
        
        self.automata.push_node(tl_i5_i6_s5_s6)
        self.automata.push_node(p_sb1_sb2)
    
    def operation_T_L1(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "T_L":
            raise ValueError("Unexpected top node in machine stack")
        
        sb1_p = Sintetized("sb1")
        sb2_p = Sintetized("sb2")
        
        ima_mult = Inherited("ima")
        imb_mult = Inherited("imb")
        imc_mult = Inherited("imc")
        imd_mult = Inherited("imd")
        
        sm_mult = Sintetized("sm")
        sem_mult = Sintetized("sem")
        
        i7_tl = Inherited("i7")
        i8_tl = Inherited("i8")
        
        s7_tl = Sintetized("s7")
        s8_tl = Sintetized("s8")
        
        term_mult = Terminal("symbol", "*")
        
        p_sb1_sb2 = NoTerminal("P")
        p_sb1_sb2.sintetized.append(sb1_p)
        p_sb1_sb2.sintetized.append(sb2_p)
        
        mult = Action("Mult")
        mult.inherited.append(ima_mult)
        mult.inherited.append(imb_mult)
        mult.inherited.append(imc_mult)
        mult.inherited.append(imd_mult)
        mult.sintetized.append(sm_mult)
        mult.sintetized.append(sem_mult) 
        
        tl_i7_i8_s7_s8 = NoTerminal("T_L")
        tl_i7_i8_s7_s8.inherited.append(i7_tl)
        tl_i7_i8_s7_s8.inherited.append(i8_tl)
        tl_i7_i8_s7_s8.sintetized.append(s7_tl)
        tl_i7_i8_s7_s8.sintetized.append(s8_tl)
        
        ima_mult.value = tope_pila.inherited[0].value                           # ima <- i5
        imb_mult.ref = sb1_p                                                    # imb <- sb1
        sb1_p.attr_users.append(imb_mult)
        imc_mult.value = tope_pila.inherited[1].value                           # imc <- i6
        imd_mult.ref = sb2_p                                                    # imd <- sb2
        sb2_p.attr_users.append(imd_mult)
        
        mult.add_exec(lambda ima, imb, sm: setattr(sm, "ref", Terminal("sm", ima.value * imb.value)), ima_mult, imb_mult, snt_dest=sm_mult)
        mult.add_exec(lambda imc, imd, sem: setattr(sem, "ref", Terminal("sem", f"{imc.value}*{imd.value}")), imc_mult, imd_mult, snt_dest=sem_mult)         
      
        i7_tl.ref = sm_mult                                                     # i7 <- sm
        sm_mult.attr_users.append(i7_tl)
        i8_tl.ref = sem_mult                                                    # i8 <- sem
        sem_mult.attr_users.append(i8_tl)
        
        s7_tl.attr_users.append(tope_pila.sintetized[0])                        # s5 <- s7: Se deja pendiente para propagación de valores
        s8_tl.attr_users.append(tope_pila.sintetized[1])                        # s6 <- s8: Se deja pendiente para propagación de valores
        
        self.automata.push_node(tl_i7_i8_s7_s8)
        self.automata.push_node(mult)
        self.automata.push_node(p_sb1_sb2)
        self.automata.push_node(term_mult)
        
    def operation_T_L2(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "T_L":
            raise ValueError("Unexpected top node in machine stack")
        
        sb1_p = Sintetized("sb1")
        sb2_p = Sintetized("sb2")
        
        ida_div = Inherited("ida")
        idb_div = Inherited("idb")
        idc_div = Inherited("idc")
        idd_div = Inherited("idd")
        
        sd_div = Sintetized("sd")
        sed_div = Sintetized("sed")
        
        i7_tl = Inherited("i7")
        i8_tl = Inherited("i8")
        
        s7_tl = Sintetized("s7")
        s8_tl = Sintetized("s8")
        
        term_div = Terminal("symbol", "/")
        
        p_sb1_sb2 = NoTerminal("P")
        p_sb1_sb2.sintetized.append(sb1_p)
        p_sb1_sb2.sintetized.append(sb2_p)
        
        div = Action("Div")
        div.inherited.append(ida_div)
        div.inherited.append(idb_div)
        div.inherited.append(idc_div)
        div.inherited.append(idd_div)
        div.sintetized.append(sd_div)
        div.sintetized.append(sed_div) 
        
        tl_i7_i8_s7_s8 = NoTerminal("T_L")
        tl_i7_i8_s7_s8.inherited.append(i7_tl)
        tl_i7_i8_s7_s8.inherited.append(i8_tl)
        tl_i7_i8_s7_s8.sintetized.append(s7_tl)
        tl_i7_i8_s7_s8.sintetized.append(s8_tl)
        
        ida_div.value = tope_pila.inherited[0].value                            # ida <- i5
        idb_div.ref = sb1_p.ref                                                 # idb <- sb1
        sb1_p.attr_users.append(idb_div)
        idc_div.value = tope_pila.inherited[1].value                            # idc <- i6
        idd_div.ref = sb2_p                                                     # idd <- sb2
        sb2_p.attr_users.append(idd_div)
        
        div.add_exec(lambda ida, idb, sd: setattr(sd, "ref", Terminal("sd", ida.value / idb.value)), ida_div, idb_div, snt_dest=sd_div)
        div.add_exec(lambda idc, idd, sed: setattr(sed, "ref", Terminal("sed", f"{idc.value}/{idd.value}")), idc_div, idd_div, snt_dest=sed_div)         
      
        i7_tl.ref = sd_div                                                      # i7 <- sd
        sd_div.attr_users.append(i7_tl)
        i8_tl.ref = sed_div                                                     # i8 <- sed
        sed_div.attr_users.append(i8_tl)
        
        s7_tl.attr_users.append(tope_pila.sintetized[0])                        # s5 <- s7: Se deja pendiente para propagación de valores
        s8_tl.attr_users.append(tope_pila.sintetized[1])                        # s6 <- s8: Se deja pendiente para propagación de valores
        
        self.automata.push_node(tl_i7_i8_s7_s8)
        self.automata.push_node(div)
        self.automata.push_node(p_sb1_sb2)
        self.automata.push_node(term_div)   
    
    def operation_T_L3(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "T_L":
            raise ValueError("Unexpected top node in machine stack")
        
        tope_pila.sintetized[0].ref = tope_pila.inherited[0]                    # s7 <- i7
        tope_pila.inherited[0].attr_users.append(tope_pila.sintetized[0])
        tope_pila.sintetized[1].ref = tope_pila.inherited[1]                    # s8 <- i8
        tope_pila.inherited[1].attr_users.append(tope_pila.sintetized[1])
        
        self.automata.push_node(Terminal("special", "$"))                       # Hay que apilar el vacío (XD)
    
    def operation_P(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "P":
            raise ValueError("Unexpected top node in machine stack")
        
        sc1_f = Sintetized("sc1")
        sc2_f = Sintetized("sc2")
        
        i9_pl = Inherited("i9")
        i10_pl = Inherited("i10")
        
        s9_pl = Sintetized("s9")
        s10_pl = Sintetized("s10")
        
        f_sc1_sc2 = NoTerminal("F")
        f_sc1_sc2.sintetized.append(sc1_f)
        f_sc1_sc2.sintetized.append(sc2_f)
        
        pl_i9_i10_s9_s10 = NoTerminal("P_L")
        pl_i9_i10_s9_s10.inherited.append(i9_pl)
        pl_i9_i10_s9_s10.inherited.append(i10_pl)
        pl_i9_i10_s9_s10.sintetized.append(s9_pl)
        pl_i9_i10_s9_s10.sintetized.append(s10_pl)
        
        i9_pl.ref = sc1_f                                                       # i9  <- sc1
        sc1_f.attr_users.append(i9_pl)
        i10_pl.ref = sc2_f                                                      # i10 <- sc2
        sc2_f.attr_users.append(i10_pl)
        s9_pl.attr_users.append(tope_pila.sintetized[0])                        # sb1 <- s9:  Se deja pendiente para propagación de valores
        s10_pl.attr_users.append(tope_pila.sintetized[1])                       # sb2 <- s10: Se deja pendiente para propagación de valores
        
        self.automata.push_node(pl_i9_i10_s9_s10)
        self.automata.push_node(f_sc1_sc2)
    
    def operation_P_L1(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "P_L":
            raise ValueError("Unexpected top node in machine stack")
        
        sc1_f = Sintetized("sc1")
        sc2_f = Sintetized("sc2")
        
        ipa_pot = Inherited("ipa")
        ipb_pot = Inherited("ipb")
        ipc_pot = Inherited("ipc")
        ipd_pot = Inherited("ipd")
        
        sp_pot = Sintetized("sp")
        sep_pot = Sintetized("sep")
        
        i11_pl = Inherited("i11")
        i12_pl = Inherited("i12")
        
        s11_pl = Sintetized("s11")
        s12_pl = Sintetized("s12")
        
        term_pot = Terminal("symbol", "^")
        
        f_sc1_sc2 = NoTerminal("P")
        f_sc1_sc2.sintetized.append(sc1_f)
        f_sc1_sc2.sintetized.append(sc2_f)
        
        pot = Action("Pot")
        pot.inherited.append(ipa_pot)
        pot.inherited.append(ipb_pot)
        pot.inherited.append(ipc_pot)
        pot.inherited.append(ipd_pot)
        pot.sintetized.append(sp_pot)
        pot.sintetized.append(sep_pot) 
        
        pl_i11_i12_s11_s12 = NoTerminal("P_L")
        pl_i11_i12_s11_s12.inherited.append(i11_pl)
        pl_i11_i12_s11_s12.inherited.append(i12_pl)
        pl_i11_i12_s11_s12.sintetized.append(s11_pl)
        pl_i11_i12_s11_s12.sintetized.append(s12_pl)
        
        ipa_pot.value = tope_pila.inherited[0].value                            # ipa <- i9
        ipb_pot.ref = sc1_f                                                     # ipb <- sc1
        sc1_f.attr_users.append(ipb_pot)
        ipc_pot.value = tope_pila.inherited[1].value                            # ipc <- i10
        ipd_pot.ref = sc2_f                                                     # ipd <- sc2
        sc2_f.attr_users.append(ipd_pot)
        
        pot.add_exec(lambda ipa, ipb, sp: setattr(sp, "ref", Terminal("sp", ipa.value ** ipb.value)), ipa_pot, ipb_pot, snt_dest=sp_pot)
        pot.add_exec(lambda ipc, ipd, sep: setattr(sep, "ref", Terminal("sep", f"{ipc.value}^{ipd.value}")), ipc_pot, ipd_pot, snt_dest=sep_pot)         
      
        i11_pl.ref = sp_pot                                                     # i11 <- sp
        sp_pot.attr_users.append(i11_pl)
        i12_pl.ref = sep_pot                                                    # i12 <- sep
        sep_pot.attr_users.append(i12_pl)
        
        s11_pl.attr_users.append(tope_pila.sintetized[0])                       # s9  <- s11: Se deja pendiente para propagación de valores
        s12_pl.attr_users.append(tope_pila.sintetized[1])                       # s10 <- s12: Se deja pendiente para propagación de valores
        
        self.automata.push_node(pl_i11_i12_s11_s12)
        self.automata.push_node(pot)
        self.automata.push_node(f_sc1_sc2)
        self.automata.push_node(term_pot)   
    
    def operation_P_L2(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "P_L":
            raise ValueError("Unexpected top node in machine stack")
                
        tope_pila.sintetized[0].ref = tope_pila.inherited[0]                    # s11 <- i11
        tope_pila.inherited[0].attr_users.append(tope_pila.sintetized[0])
        tope_pila.sintetized[1].ref = tope_pila.inherited[1]                    # s12 <- i12
        tope_pila.inherited[1].attr_users.append(tope_pila.sintetized[1])
        
        self.automata.push_node(Terminal("special", "$"))                       # Hay que apilar el vacío (XD)
        
    def operation_F1(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "F":
            raise ValueError("Unexpected top node in machine stack")
        
        sv1_e = Sintetized("sv1")
        sv2_e = Sintetized("sv2")
        
        if_fillprt = Inherited("if")
        sf_fillprt = Sintetized("sf")
        
        term_pi = Terminal("symbol", "(")
        
        e_sv1_sv2 = NoTerminal("E")
        e_sv1_sv2.sintetized.append(sv1_e)
        e_sv1_sv2.sintetized.append(sv2_e)
        
        fillprt = Action("Fill_Prt")
        fillprt.inherited.append(if_fillprt)
        fillprt.sintetized.append(sf_fillprt)
        
        term_pd = Terminal("symbol", ")")
        
        sv1_e.attr_users.append(tope_pila.sintetized[0])                       # sc1 <- sv1: Se deja pendiente para propagación de valores
        if_fillprt.ref = sv2_e                                                 # if <- sv2
        sv2_e.attr_users.append(if_fillprt)
        
        fillprt.add_exec(lambda iff, sff: setattr(sff, "ref", Terminal("sf", f"({iff.value})")), if_fillprt, snt_dest=sf_fillprt)
        
        sf_fillprt.attr_users.append(tope_pila.sintetized[1])                  # sc2 <- sf: Se deja pendiente para propagación de valores
        
        self.automata.push_node(term_pd)
        self.automata.push_node(fillprt)
        self.automata.push_node(e_sv1_sv2)
        self.automata.push_node(term_pi)
        
    def operation_F2(self):
        tope_pila: NoTerminal = self.automata.top.node

        if tope_pila.name != "F":
            raise ValueError("Unexpected top node in machine stack")
        
        term_id = Terminal("id")
        
        tope_pila.sintetized[0].ref = Inherited("val", term_id.value)           # sc1 <- id.val
        tope_pila.sintetized[1].ref = Inherited("val", f"{term_id.value}")      # sc2 <- f"{id.val}"
        
        self.automata.push_node(term_id)
    
    def reload_values(self, id_nt=False):
        print("\n\nPROPAGACIÓN DE VALORES\n\n")
        
        aux = self.automata.top
        aux_node: Terminal | NoTerminal | Action
        
        first_iteration = not id_nt
        ter = None
        
        while True:
            aux_node = aux.node
                  
            print(f"{aux_node=}\n")
            
            if type(aux_node).__name__ in ("NoTerminal", "Action"):                 
                if type(aux_node).__name__ == "Action" and len(aux_node.sintetized) == 0 and aux_node.all_executed:
                    self.automata.pop_node()                                   # Saca el símbolo de acción         
                    self.automata.pop_node()                                   # Saca el axioma
                    return
                
                # Fuente: Heredado
                for aux_inh in aux_node.inherited:
                    if len(aux_inh.attr_users) == 0:
                        break
                    
                    # Destino: Heredado
                    if aux_inh.ref is not None:
                        print(f"{aux_inh.ref=}")
                        if aux_inh.ref.ref.value is not None:
                            aux_inh.value = aux_inh.ref.ref.value
                            print(f"Nuevo {aux_inh.value=}")
                            
                            # Destino: Sintetizado
                            print(f"Users: {aux_inh.attr_users} en {aux_inh}")
                            
                            for user in aux_inh.attr_users:
                                print(f"Para {user} con Valor {aux_inh.value=}")  
                                
                                user.ref = aux_inh
                                
                                print(f"Nueva asignación {user.ref.value=}")

                print(f"{aux_node.sintetized=}")
                
                valid_refs = False
                
                # Fuente: Sintetizado            
                for aux_snt in aux_node.sintetized:
                    if len(aux_snt.attr_users) == 0:
                        return
                    
                    print(f"Users de attr {aux_snt=}: {aux_snt.attr_users}")
                    
                    if aux_snt.ref is not None:
                        valid_refs = True
                        
                        for user in aux_snt.attr_users:
                            print(f"Para {user} con Referencia user.ref ={user.ref if user.ref is not None else "None"} y nueva referencia {aux_snt.ref=}")
                            
                            # Destino: Heredado
                            if type(user).__name__ == "Inherited":
                                user.ref = aux_snt
                                user.value = user.ref.ref.value
                                print(f"Nuevo valor: {user.value=}")
                            
                            # Destino: Sintetizado
                            elif type(user).__name__ == "Sintetized":
                                user.ref = aux_snt.ref 
                                print(f"Nueva conexión: {user.ref.value=}") 
                            
                            else: 
                                raise TypeError("Unexpected attr_user type")
                            
                if not valid_refs:
                    if id_nt:
                        self.automata.pop_node()
                    
                    if ter is not None:
                        self.automata.pop_node()
                        self.automata.push_node(ter.node)
                    return
                            
                print(f"Nuevo {aux_node=}\n")
                
                if first_iteration:
                    self.automata.pop_node()
                else:
                    first_iteration = True
                    
                aux = aux.lower
            else:
                ter = aux
                aux = aux.lower
                                        
                                
    def execute_analysis(self):
        NOT_EQUALS = -1
        FAMILY_EQUALS = 0
        COMPLETELY_EQUALS = 1
        
        RETIENE = False
        AVANCE = True
        
        avance_cinta = AVANCE
        tope_cinta: Terminal
        
        print("\nAXIOMA\n")
        self.axiom()
        
        while True:
            if self.automata.is_empty():
                return
            
            if avance_cinta == AVANCE:
                aux_cinta = self.input_tape.dequeue_node()
                
                if aux_cinta is not None:
                    tope_cinta = aux_cinta.node
                else:
                    tope_cinta = Terminal("special", "$")
                
            print(f"\n\n{"-"*90}\nInicio de Cinta: {tope_cinta}\nPila: ▼, {self.automata}\n\n")
            
            top_type = type(self.automata.top.node).__name__
            
            if top_type == "NoTerminal":
                avance_cinta = RETIENE
                
                match self.automata.top.node.name:
                    case "S":
                        if tope_cinta.equals_terminal(Terminal("symbol", "(")) == COMPLETELY_EQUALS or tope_cinta.equals_terminal(Terminal("id")) == FAMILY_EQUALS:
                            self.operation_S()
                            print("EJECUTÓ S\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set")
                    case "E":
                        if tope_cinta.equals_terminal(Terminal("symbol", "(")) == COMPLETELY_EQUALS or tope_cinta.equals_terminal(Terminal("id")) == FAMILY_EQUALS:
                            self.operation_E()
                            print("EJECUTÓ E\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set") 
                    case "E_L":
                        if tope_cinta.equals_terminal(Terminal("symbol", "+")) == COMPLETELY_EQUALS:
                            self.operation_E_L1()
                            print("EJECUTÓ E_L de +\n\n")
                        elif tope_cinta.equals_terminal(Terminal("symbol", "-")) == COMPLETELY_EQUALS:
                            self.operation_E_L2()
                            print("EJECUTÓ E_L de -\n\n")
                        elif self.input_tape.is_empty() or tope_cinta.equals_terminal(Terminal("symbol", ")")) == COMPLETELY_EQUALS:
                            self.operation_E_L3()
                            print("EJECUTÓ E_L VACÍO\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set")  
                    case "T":
                        if tope_cinta.equals_terminal(Terminal("symbol", "(")) == COMPLETELY_EQUALS or tope_cinta.equals_terminal(Terminal("id")) == FAMILY_EQUALS:
                            self.operation_T()
                            print("EJECUTÓ T\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set") 
                    case "T_L":
                        if tope_cinta.equals_terminal(Terminal("symbol", "*")) == COMPLETELY_EQUALS:
                            self.operation_T_L1()
                            print("EJECUTÓ T_L de *\n\n")
                        elif tope_cinta.equals_terminal(Terminal("symbol", "/")) == COMPLETELY_EQUALS:
                            self.operation_T_L2()
                            print("EJECUTÓ T_L de /\n\n")
                        elif self.input_tape.is_empty() or any(
                            tope_cinta.equals_terminal(Terminal("symbol", term)) == COMPLETELY_EQUALS for term in ("+", "-", ")")):
                            self.operation_T_L3()
                            print("EJECUTÓ T_L VACÍO\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set")  
                    case "P":
                        if tope_cinta.equals_terminal(Terminal("symbol", "(")) == COMPLETELY_EQUALS or tope_cinta.equals_terminal(Terminal("id")) == FAMILY_EQUALS:
                            self.operation_P()
                            print("EJECUTÓ P\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set") 
                    case "P_L":
                        if tope_cinta.equals_terminal(Terminal("symbol", "^")) == COMPLETELY_EQUALS:
                            self.operation_P_L1()
                            print("EJECUTÓ P_L de ^\n\n")
                        elif self.input_tape.is_empty() or any(
                            tope_cinta.equals_terminal(Terminal("symbol", term)) == COMPLETELY_EQUALS for term in ("+", "-", "*", "/", ")")):
                            self.operation_P_L2()
                            print("EJECUTÓ P_L VACÍO\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set")  
                    case "F":
                        if tope_cinta.equals_terminal(Terminal("symbol", "(")) == COMPLETELY_EQUALS:
                            self.operation_F1()
                            print("EJECUTÓ F de (exp)\n\n")
                        elif tope_cinta.equals_terminal(Terminal("id")) == FAMILY_EQUALS:
                            self.operation_F2()
                            print("EJECUTÓ F de id\n\n")
                        else:
                            print("El elemento de la cinta no cumple con el conjunto solución. RECHACE LA SECUENCIA.")
                            raise ValueError("Tape element not in solution set")  
                    case _:
                        return
            
            elif top_type == "Action":
                avance_cinta = RETIENE
                
                self.automata.top.node.exec()
                self.reload_values()
            
            elif top_type == "Terminal":
                empty_string_in_topnode = self.automata.top.node.equals_terminal(Terminal("special", "$")) == COMPLETELY_EQUALS
                avance_cinta = not empty_string_in_topnode
                id_is_nt = False
                
                if self.automata.top.node.equals_terminal(tope_cinta) == FAMILY_EQUALS or empty_string_in_topnode:
                    if self.automata.top.node.equals_terminal(tope_cinta) == FAMILY_EQUALS:
                        id_is_nt = True
                        
                        self.automata.pop_node()
                        self.automata.top.node.sintetized[0].ref = tope_cinta
                        self.automata.top.node.sintetized[1].ref = tope_cinta
                    
                    elif empty_string_in_topnode:
                        self.automata.pop_node()
                    
                    self.reload_values(id_nt=id_is_nt)
                elif self.automata.top.node.equals_terminal(tope_cinta) == COMPLETELY_EQUALS and not empty_string_in_topnode:
                    self.automata.pop_node()
                else:
                    print("No coincide elemento de cinta de entrada con elemento de pila. Falla el Análisis Sintáctico. RECHACE LA SECUENCIA")
                    raise ValueError("Pile top and Input Tape first element mismatch")
            else:
                raise TypeError("Unknown type detected")
            
            print(f"\nPila: ▼, {self.automata}\nOp.Cinta: {"AVANCE" if avance_cinta == AVANCE else "RETIENE"}\n\n")
            # os.system("echo Presione Enter para continuar...&pause>nul")
        

if __name__ == "__main__":
    stape = Queue("Cinta de Entrada")
    
    # 84 + 12 / (4 ^ 2 + 8) - 7 * 3
    
    stape.enqueue_node(Terminal("id", 84))
    stape.enqueue_node(Terminal("symbol", "+"))
    stape.enqueue_node(Terminal("id", 12))
    stape.enqueue_node(Terminal("symbol", "/"))
    stape.enqueue_node(Terminal("symbol", "("))
    stape.enqueue_node(Terminal("id", 4))
    stape.enqueue_node(Terminal("symbol", "^"))
    stape.enqueue_node(Terminal("id", 2))
    stape.enqueue_node(Terminal("symbol", "+"))
    stape.enqueue_node(Terminal("id", 8))
    stape.enqueue_node(Terminal("symbol", ")"))
    stape.enqueue_node(Terminal("symbol", "-"))
    stape.enqueue_node(Terminal("id", 7))
    stape.enqueue_node(Terminal("symbol", "*"))
    stape.enqueue_node(Terminal("id", 3))
    
    aux_lex = Lexical()
    aux_lex.set_stringtape(stape)
    
    gram = Practica2(aux_lex)
    