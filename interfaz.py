from tkinter import Tk, Frame, Label, Entry, Button, Text, END, Scrollbar
from tkinter.ttk import Combobox
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate
import matplotlib.pyplot as m
from numpy import linspace, sin, cos, e
from metodos_calculo_raices import regla_falsa, newton_raphson, biseccion, metodo_de_la_secante

f = lambda x: x ** 3 + 4 * x ** 2 - 10
df = lambda x: 3 * x ** 2 + 8 * x

g = lambda x: x ** 3 - 2 * x ** 2 - 5
dg = lambda x: 3 * x ** 2 - 4 * x

h = lambda x: x ** 3 + 3 * x ** 2 - 1
dh = lambda x: 3 * x ** 2 + 6 * x

k = lambda x: x - cos(x)
dk = lambda x: 1 + sin(x)

l = lambda x: e * x + 2 - x + 2 * cos(x) - 6
dl = lambda x: -2 * sin(x) + e - 1


class Interfaz:

    def __init__(self) -> None:
        
        self.tabla = list()
        self.encabezado = list()
        self.funciones = [f, g, h, k, l]
        self.derivadas = [df, dg, dh, dk, dl]

        self.raiz = Tk()
        self.raiz.title("Búsqueda de Raíces")
        self.raiz.resizable(0, 1)

        self.marco = Frame(self.raiz)
        self.marco.pack()

        Label(self.marco, text="Función").grid(row=0, column=0, padx=10)
        self.menu_funciones = Combobox(self.marco)
        self.menu_funciones['values'] = ("x^3+4x^2-10", "x^3-2x^2-5", "x^3+3x^2-1", "x-cos(x)", "e*x+2-x+2cos(x)-6")
        self.menu_funciones.current(0)
        self.menu_funciones.grid(row=0, column=1, pady=10)

        Label(self.marco, text="Límite inferior a").grid(row=0, column=2)
        self.campo_a = Entry(self.marco)
        self.campo_a.config(justify="center")
        self.campo_a.grid(row=0, column=3)

        Label(self.marco, text="Límite superior b").grid(row=0, column=4)
        self.campo_b = Entry(self.marco)
        self.campo_b.config(justify="center")
        self.campo_b.grid(row=0, column=5)

        Label(self.marco, text="Número puntos").grid(row=0, column=6)
        self.campo_puntos = Entry(self.marco)
        self.campo_puntos.config(justify="center")
        self.campo_puntos.grid(row=0, column=7)

        Label(self.marco, text="Iteraciones").grid(row=0, column=8)
        self.campo_ite = Entry(self.marco)
        self.campo_ite.config(justify="center")
        self.campo_ite.grid(row=0, column=9)

        Label(self.marco, text="Método").grid(row=1, column=0)
        self.menu_metodos = Combobox(self.marco)
        self.menu_metodos['values'] = ("Bisección", "Newton-Raphson", "De la Secante", "De la Regla Falsa", "De Müller")
        self.menu_metodos.grid(row=1, column=1)
        self.menu_metodos.bind("<<ComboboxSelected>>", self.segun_metodo)

        Label(self.marco, text="Aproximación p0").grid(row=1, column=2)
        self.campo_aproximacion_0 = Entry(self.marco)
        self.campo_aproximacion_0.config(justify="center")
        self.campo_aproximacion_0.grid(row=1, column=3)

        Label(self.marco, text="Aproximación p1").grid(row=1, column=4)
        self.campo_aproximacion_1 = Entry(self.marco)
        self.campo_aproximacion_1.config(justify="center")
        self.campo_aproximacion_1.grid(row=1, column=5)

        Label(self.marco, text="Aproximación p2").grid(row=1, column=6)
        self.campo_aproximacion_2 = Entry(self.marco)
        self.campo_aproximacion_2.config(justify="center")
        self.campo_aproximacion_2.grid(row=1, column=7)

        Label(self.marco, text="Toleracia").grid(row=1, column=8)
        self.campo_tol = Entry(self.marco)
        self.campo_tol.config(justify="center")
        self.campo_tol.grid(row=1, column=9)

        self.boton_graficar = Button(self.marco, text="Buscar Raíz", command=self.calcular_raiz)
        self.boton_graficar.grid(row=3, column=9, padx=10)
        self.boton_graficar.config(width=15)

        self.figura = m.Figure(figsize=(7, 5), dpi=90)
        self.ax = self.figura.add_subplot(111)
        self.ax.grid(True)
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y(x)$')
        self.ax.set_title("Búsqueda de Raíces")
        self.ax.axhline(0, color="black")
        self.ax.axvline(0, color="black")

        self.linea = FigureCanvasTkAgg(self.figura, self.marco)
        self.linea.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, columnspan=5)
        self.barra_navegacion = NavigationToolbar2Tk(self.linea, self.raiz)
        self.barra_navegacion.update()

        self.contenedor_tabla = Text(self.marco, width=72, height=28)
        self.contenedor_tabla.grid(row=2, column=5, padx=10, pady=10, columnspan=5)

        Label(self.marco, text="Raíz").grid(row=3, column=5)
        self.campo_raiz = Entry(self.marco, width=45)
        self.campo_raiz.config(justify="center")
        self.campo_raiz.grid(row=3, column=6, columnspan=2)

        self.raiz.mainloop()

    def calcular_raiz(self):
        self.contenedor_tabla.delete("1.0", END)
        self.tabla.clear()
        a = float(self.campo_a.get())
        b = float(self.campo_b.get())
        puntos = int(self.campo_puntos.get())
        tol = float(self.campo_tol.get())
        no = int(self.campo_ite.get())
        funcion = self.menu_funciones.current()
        metodo = self.menu_metodos.current()
        self.campo_raiz.delete(0, END)
        self.ax.clear()
        x = linspace(a, b, puntos)
        y = self.funciones[funcion](x)
        etiqueta = "$"+self.menu_funciones.get()+"$"
        self.ax.plot(x, y, label=etiqueta)
        if metodo == 0:
            completado, solucion = biseccion(self.funciones[funcion], a, b, tol, no)
            self.tabla = solucion
            if completado:
                self.campo_raiz.insert(0, solucion[len(solucion)-1][3])
                for punto in solucion:
                    etiqueta = "$p_{" + str(punto[0]) + "}$"
                    self.ax.plot(punto[3], 0, marker="o", label=etiqueta)
        elif metodo == 1:
            p0 = float(self.campo_aproximacion_0.get())
            completado, solucion = newton_raphson(self.funciones[funcion], self.derivadas[funcion], p0, tol, no)
            self.tabla = solucion
            if completado:
                self.campo_raiz.insert(0, solucion[len(solucion)-1][2])
                for punto in solucion:
                    x = [punto[1], punto[2]]
                    y = [punto[3], 0]
                    etiqueta = "$p_{" + str(punto[0]) + "}$"
                    self.ax.plot(x, y, marker="o", label=etiqueta, color=f'C{punto[0]}')                
        elif metodo == 2:
            p0 = float(self.campo_aproximacion_0.get())
            p1 = float(self.campo_aproximacion_1.get())
            completado, solucion = metodo_de_la_secante(self.funciones[funcion], p0, p1, tol, no)
            self.tabla = solucion
            if completado:
                self.campo_raiz.insert(0, solucion[len(solucion)-1][2])
                for punto in solucion:
                    etiqueta = "$p_{" + str(punto[0]) + "}$"
                    x = [punto[1], punto[2]]
                    y = [punto[3], punto[4]]
                    self.ax.plot(x, y, marker="o", label=etiqueta, linewidth=1)
        elif metodo == 3:
            p0 = float(self.campo_aproximacion_0.get())
            p1 = float(self.campo_aproximacion_1.get())
            completado, solucion = regla_falsa(self.funciones[funcion], p0, p1, tol, no)
            self.tabla = solucion
            if completado:
                self.campo_raiz.insert(0, solucion[len(solucion)-1][2])
                for punto in solucion:
                    etiqueta = "$p_{" + str(punto[0]) + "}$"
                    x = [punto[1], punto[2]]
                    y = [punto[3], punto[4]]
                    self.ax.plot(x, y, marker="o", label=etiqueta, linewidth=1)

        self.contenedor_tabla.insert(1.0, tabulate(self.tabla, tablefmt='simple', headers=self.encabezado))
        self.ax.set_xlim([a, b])
        self.ax.grid(True)
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y(x)$')
        self.ax.set_title("Búsqueda de Raíces")
        self.ax.axhline(0, color="black")
        self.ax.axvline(0, color="black")
        self.ax.legend(loc=2)
        self.linea.draw()

    def segun_metodo(self, evento):
        self.campo_aproximacion_0.config(state="normal")
        self.campo_aproximacion_1.config(state="normal")
        self.campo_aproximacion_2.config(state="normal")
        self.encabezado.clear()
        opcion = self.menu_metodos.get()
        if opcion == "Bisección":
            self.campo_aproximacion_0.config(state="disable")
            self.campo_aproximacion_1.config(state="disable")
            self.campo_aproximacion_2.config(state="disable")
            self.encabezado = ["n", "a", "b", "m", "f(a)", "f(b)", "f(m)", "Error"]
        elif opcion == "Newton-Raphson":
            self.campo_aproximacion_1.config(state="disable")
            self.campo_aproximacion_2.config(state="disable")
            self.encabezado = ["n", "pi", "pi+1", "f(pi)", "f(pi+1)", "Error"]
        elif opcion == "De la Secante" or opcion == "De la Regla Falsa":
            self.campo_aproximacion_2.config(state="disable")
            self.encabezado = ["n", "pi", "pi+1", "f(pi)", "f(pi+1)", "Error"]


if __name__ == "__main__":
    Interfaz()

