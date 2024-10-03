import flet as ft

# Dados
dummy_data: dict[int, dict[str, any]] = {
    0: {"name": "Apple", "description": "Red and juicy", "quantity": 5, "price": 1.99},
    1: {"name": "Bread", "description": "Whole wheat loaf", "quantity": 2, "price": 3.49},
    2: {"name": "Milk", "description": "Organic whole milk", "quantity": 1, "price": 2.99},
    3: {"name": "Carrot", "description": "Fresh and crunchy", "quantity": 10, "price": 0.99},
    4: {"name": "Eggs", "description": "Free-range brown eggs", "quantity": 12, "price": 2.79},
    5: {"name": "Chicken", "description": "Boneless skinless breasts", "quantity": 2, "price": 7.99},
    6: {"name": "Banana", "description": "Ripe and yellow", "quantity": 6, "price": 0.49},
}

class Controller:
    items: dict = dummy_data
    counter: int = len(items)

    @staticmethod
    def get_items() -> dict:
        return Controller.items
    
    @staticmethod
    def add_items(data: dict) -> None:
        Controller.items[Controller.counter] = data
        Controller.counter += 1

# Define o stilo e atributos
header_style: dict[str, any] ={
    "height": 60,
    "bgcolor": "#081d33",
    "border_radius": ft.border_radius.only(top_left=15, top_right=15),
    "padding": ft.padding.only(left=15, right=15),
}

# Um metodo que cria e retorna um campo de texto
def search_field(function: callable) -> ft.TextField:
    return ft.TextField(
        border_color="transparent",
        height=20,
        text_size=14,
        content_padding=0,
        cursor_color="white",
        cursor_width=1,
        color="white",
        hint_text="Pesquisa",
        on_change=function,
    )

# Um metodo que adiciona um contener ao campo de pesquisa
def search_bar(control: ft.TextField):
    return ft.Container(
        width=350,
        bgcolor="white10",
        border_radius=6,
        opacity=0,
        animate_opacity=300,
        padding=8,
        content=ft.Row(
            spacing=10,
            vertical_alignment="center",
            controls=[
                ft.Icon(
                    name=ft.icons.SEARCH_ROUNDED,
                    size=17,
                    opacity=0.85,
                ),
                control,
            ],
        ),
    )

# Define a class cabeçalho
class Header(ft.Container):
    def __init__(self, dt: 'DataTable') -> None:
        super().__init__(**header_style, on_hover=self.toggles_search)

        # Crea dt
        self.dt: 'DataTable' = dt
        # Cria um TextField para buscar/Filtro
        self.search_value: ft.TextField = search_field(self.filter_df_rows)
        self.search: ft.Container = search_bar(self.search_value)

        # Define outras classes e atribultos
        self.name = ft.Text("Line Indent")           #Linha recuada
        self.avatar = ft.IconButton("Person")        # Pessoa

        # Atributos
        self.content = ft.Row(
            alignment="spaceBetween", controls=[self.name, self.search, self.avatar]
        )

    # Definir método que alterna a visibilidade da caixa de pesquisa
    def toggles_search(self, e: ft.HoverEvent) -> None:
        self.search.opacity = 1 if e.data == "true" else 0
        self.search.update()

    # define um metodo de espaco reservado para filtrar dados
    def filter_df_rows(self, e):
        # finalmente,posso filtar os dados

        #precisamos acessar as linhas da instancia da tabela de dados
        search_term = e.control.value.lower()
        #final
        for data_rows in self.dt.rows:
            #estou apenas ajustando com base na coluna um
            #entao apenas a primeira posição do indice [0]
            data_cell = data_rows.cells[0]
            #alteramos a visivilidade 
            #lidamos com a distrinção entre maiusculas e minusculas
            data_rows.visible = search_term in data_cell.content.value.lower()

            data_rows.update()

#Define estilo e atributos de classe de formulario
form_style: dict[str, any] = {
    "border_radius": 8,
    "border": ft.border.all(1, "#ebebeb"),
    "bgcolor": "white10",
    "padding": 15,
}

# Define um método que cria e retorna um campo de texto
def text_field() -> ft.TextField:
    return ft.TextField(
        border_color="transparent",
        height=20,
        text_size=13,
        content_padding=0,
        cursor_color="black",
        cursor_height=18,
        cursor_width=1,
        color="black",
)


# Define um contener para envolver o campo de texto
def text_field_container(
        expand: bool | int, name: str, control: ft.TextField
) -> ft.Container:
    return ft.Container(
        expand=expand,
        height=45,
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        content=ft.Column(
            spacing=1,
            controls=[
                ft.Text(
                    value=name,
                    size=9,
                    color="black",
                    weight="bold"
                ),
                control
            ]
        )
)



# Proximo, define uma classe de formulario
class Form(ft.Container):
    def __init__(self, dt: 'DataTable') -> None:
        super().__init__(**form_style)
        
        self.dt = dt

        #define 4 rows
        self.row1_value: ft.TextField = text_field()
        self.row2_value: ft.TextField = text_field()
        self.row3_value: ft.TextField = text_field()
        self.row4_value: ft.TextField = text_field()

        # Envolve em contener
        self.row1: ft.Container = text_field_container(True, "Linha Um", self.row1_value)
        self.row2: ft.Container = text_field_container(True, "Linha Dois", self.row2_value)
        self.row3: ft.Container = text_field_container(True, "Linha Três", self.row3_value)
        self.row4: ft.Container = text_field_container(True, "Linha Quatro", self.row4_value)
        # Define o botao 
        self.submit = ft.ElevatedButton(
            text="Submit",              #Enviar
            style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=8)}),
            on_click=self.submit_data,
        )

        # Atributos
        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Row(controls=[self.row1]),
                ft.Row(controls=[self.row2, self.row3, self.row4]),
                ft.Row(controls=[self.submit], alignment="end"),
            ]
        )

    # define um metodo para enviar dados
    def submit_data(self, e: ft.TapEvent) -> None:
        # Obtemos o valor de cada campo de texto e criamos uma estrutura de dados para ele
        data: dict[str, str | None] = {
            "col1": self.row1_value.value,
            "col2": self.row2_value.value,
            "col3": self.row3_value.value,
            "col4": self.row4_value.value,
        }

        # proximo chamamos o controlador e adcionamos os dados
        Controller.add_items(data)

        # Por fim limpe as entrads e volta a preencher
        self.clear_entries()
        self.dt.fill_data_table()    

    # Define um metodo para limpar entrada após o envio
    def clear_entries(self) -> None:
        self.row1_value.value = ""
        self.row2_value.value = ""
        self.row3_value.value = ""
        self.row4_value.value = ""
        
        self.content.update()

# Define alguns estilos, atributos e colunas da tabela de dados
column_names: list[str] = [
    "Column One", "Column Tow", "Column Three", " Column Four",
]

data_table_style: dict[str, any] = {
    "expand": True,
    "border_radius": 8,
    "border": ft.border.all(2, "#ebebeb"),
    "horizontal_lines": ft.border.BorderSide(1, "#ebebeb"),
    "columns": [
        #list
        ft.DataColumn(ft.Text(index, size=12, color="black", 
                              weight="bold")) 
                              for index in column_names
    ]
}


# Proximo, Define a classe para a tabela de dados
class DataTable(ft.DataTable):
    def __init__(self) -> None:
        super().__init__(**data_table_style) 
        # Criar um atribulto get items
        self.df: any = Controller.get_items()
    
    def fill_data_table(self) -> None:
        # Limpa as linhas da tabela de dados para lote novo/ atualizado
        self.rows = []
        # Verifique o tipo de dados dict para entender o loop
        for values in self.df.values():
            # Cria um novo DataRow
            data = ft.DataRow(cells= [
                ft.DataCell(ft.Text(value, color="black")) for value in values.values()
                ]
            )

            self.rows.append(data)
        
        self.update()


def main(page: ft.Page) -> None:
    page.bgcolor = "#fdfdfd"

    table = DataTable()
    header = Header(dt=table)
    form = Form(dt=table)

    page.add(
        ft.Column(
            expand=True,
            controls=[
                # Cabeçalho...
                header,
                ft.Divider(height=2, color="transparent"),
                # Formulario...
                form,
                ft.Column(
                    scroll="hidden",
                    expand=True,
                    controls=[ft.Row(controls=[table])],      # Tabelas
                ),
            ],
        )
    )

    # Podemos preencher o dt depois de adicionar o controle a pagina
    table.fill_data_table()

    page.update()

if __name__=="__main__":
    ft.app(target=main)