import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from toolbox.mouse_In_excel import DataProcessor
import pickle

class Mouse:
    def __init__(self, name=None, cage_number=None, weight_list=None, date_list=None, weight_date_df=None, delta_weight=None, input_time=None, kill_time=None, kill_df=None, mouse_description=None, exception_description=None, location=None,
    input_food=None, release_food=None, mouse_kill=None):
        """
        初始化 Mouse 类的实例。

        Parameters:
            name (str): 鼠的名称。
            cage_number (int): 笼子编号。
            weight_list (list, np.ndarray, pd.Series): 包含鼠体重数据的列表、数组或 Series。
            date_list (list, pd.Series): 包含日期数据的列表或日期列。
            weight_date_df (pd.DataFrame): 包含体重和日期数据的 DataFrame。
            delta_weight (list, np.ndarray, pd.Series): 包含体重变化率的列表、数组或 Series。
            input_time (str): 鼠的录入时间。
            kill_time (str): 鼠的结束时间。
            kill_df (pd.DataFrame): 包含结束数据的 DataFrame。
            mouse_description (str): 关于鼠的描述。
            exception_description (str): 异常情况描述。
            location (str): 描述鼠所在的文件的位置
            input_food (dict): 包含进食数据的字典。
            release_food (dict): 包含剩余粮食数据的字典。
            mouse_kill (dict): 包含杀鼠表数据的字典。
        """
        self.name = name
        self.cage_number = cage_number
        self.location = location
        self.input_food = input_food
        self.release_food = release_food
        self.kill = mouse_kill

        # 初始化 weight_list
        if weight_list is not None:
            if isinstance(weight_list, (list, np.ndarray)):
                self.weight_list = weight_list
            elif isinstance(weight_list, pd.Series):
                self.weight_list = weight_list
            else:
                raise ValueError("weight_list should be a list, NumPy array, or a DataFrame column.")
        else:
            self.weight_list = None

        # 初始化 date_list
        if date_list is not None:
            if isinstance(date_list, list):
                self.date_list = pd.to_datetime(date_list, errors='coerce')
            elif isinstance(date_list, pd.Series):
                self.date_list = pd.to_datetime(date_list, errors='coerce')
            else:
                raise ValueError("date_list should be a list or a DataFrame column.")
        else:
            self.date_list = None

        # 初始化 weight_date_df，进食变化
        if weight_date_df is None:
            self.weight_date_df = self.weight2data()
        else:
            self.weight_date_df = weight_date_df

        self.delta_weight = delta_weight

        # 快速的判断和转化日期时间
        self.input_time = pd.to_datetime(input_time, errors='coerce') if input_time is not None else None
        self.kill_time = pd.to_datetime(kill_time, errors='coerce') if kill_time is not None else None

        self.kill_df = kill_df
        self.mouse_description = mouse_description
        self.exception_description = exception_description

    def weight2data(self):
        """
        创建包含粮食数量和日期数据的 DataFrame。

        Returns:
            pd.DataFrame: 包含体重和日期数据的 DataFrame。
        """
        if self.date_list is not None and self.weight_list is not None:
            data_dict = {
                "date": self.date_list,
                self.name: self.weight_list
            }
            data_df = pd.DataFrame(data_dict)
            return data_df
        else:
            raise ValueError("Both date_list and weight_list must be provided to create the DataFrame.")

    def plot_data(self, x, y, title, x_label, y_label, color):
        """
        绘制数据随时间的变化图。

        Parameters:
            x (list, np.ndarray, pd.Series): X 轴数据。
            y (list, np.ndarray, pd.Series): Y 轴数据。
            title (str): 图的标题。
            x_label (str): X 轴标签。
            y_label (str): Y 轴标签。
            color (str): 曲线颜色。
        """
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o', linestyle='-', color=color)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid(True)
        plt.show()

    def plot_weight(self):
        # 绘制体重随时间的变化图
        self.plot_data(self.weight_list.keys(), self.weight_list, f'{self.name}的体重变化', '日期', '体重', 'b')

    def plot_delta_weight(self):
        # 绘制体重变化率随时间的变化图
        self.plot_data(self.delta_weight.keys(), self.delta_weight, f'{self.name}的体重变化率', '日期', '体重变化率', 'g')

    def plot_eat_food(self):
        # 绘制每周进食情况随时间的变化图
        self.plot_data(self.weight_date_df.keys(), self.weight_date_df, f'{self.name}的进食变化', '日期', '每周的进食变化', 'g')

    def change_data(self, decide, chose, new_value, date):
        """
        根据选择的参数更改鼠的数据。

        Parameters:
            decide (str): 决定是添加数据还是删除数据。
            chose (str): 决定是更改体重记录、杀鼠表、新增粮食还是剩余粮食。
            new_value: 新的数据值。
            date: 数据的日期。
        """
        mouse_location = self.location
        if chose == "体重记录":
            sheet_name = "体重记录"
            print(self.weight_list)
        elif chose == "杀鼠表":
            sheet_name = "杀鼠表"
        elif chose == "新增粮食":
            sheet_name = "新增粮食"
            print(self.input_food)
        elif chose == "剩余粮食":
            sheet_name = "剩余粮食"
            # self.release_food = np.nan
            print(self.release_food)
            # self.release_food

    def addge_mouse(self, chose, date, value):
        """
        添加或更改鼠的数据。

        Parameters:
            chose (str): 决定是更改体重记录、杀鼠表、新增粮食还是剩余粮食。
            date: 数据的日期。
            value: 新的数据值。
        """
        # 兼顾增加新数据和改写老数据的方法
        if chose == "体重记录":
            self.weight_list[date] = value
            # print(self.weight_list)
        elif chose == "杀鼠表":
            sheet_name = "杀鼠表"
            self.kill[date] = value
        elif chose == "新增粮食":
            sheet_name = "新增粮食"
            self.input_food[date] = value
            # print(self.input_food)
        elif chose == "剩余粮食":
            sheet_name = "剩余粮食"
            # self.release_food = np.nan
            # print(self.release_food)
            self.release_food = value

    def remove_mouse(self, chose, date):
        """
        从鼠的数据中删除指定日期的记录。

        Parameters:
            chose (str): 决定是删除体重记录、杀鼠表、新增粮食还是剩余粮食的记录。
            date: 数据的日期。
        """
        if chose == "体重记录":
            if date in self.weight_list:
                del self.weight_list[date]
        elif chose == "杀鼠表":
            if date in self.kill:
                del self.kill[date]
        elif chose == "新增粮食":
            if date in self.input_food:
                del self.input_food[date]
        elif chose == "剩余粮食":
            if date in self.release_food:
                del self.release_food[date]

    def save_mouse(self, file_path="test_mouse.pkl"):
        """
        保存鼠的数据到本地文件。

        Parameters:
            file_path (str): 要保存鼠数据的文件路径。
        """
        with open(file_path, "wb") as file:
            pickle.dump(self, file)


def make_mouse(input_data="mouse-data\\test-data", output_file="out-test", mouse_number="mouse_109", mouse_cage="cage_29"):
    """
    创建 Mouse 对象并初始化它的属性。

    Parameters:
        input_data (str): 输入数据文件路径。
        output_file (str): 输出文件路径。
        mouse_number (str): 鼠的编号。
        mouse_cage (str): 笼子编号。

    Returns:
        Mouse: 初始化后的 Mouse 对象。
    """
    data_processor = DataProcessor(input_data + '.xlsx', output_file + '.xlsx')
    mouse_108 = data_processor.make_excel_mouse(mouse_number=mouse_number, mouse_food="MCD1", mouse_cage=mouse_cage)

    test_mouse = Mouse(
        name=mouse_108['name'],
        weight_date_df=mouse_108[f"{mouse_cage}的每周进食量"],
        weight_list=mouse_108[f"{mouse_number}的体重"],
        delta_weight=mouse_108[f"{mouse_number}的体重变化"],
        mouse_description=mouse_108[f"{mouse_number}的描述"],
        date_list=list(mouse_108[f"{mouse_number}的体重"].keys()),
        location=mouse_108["location"],
        input_food=mouse_108[f"{mouse_cage}的新增粮食"],
        release_food=mouse_108[f"{mouse_cage}的剩余粮食"],
        mouse_kill=mouse_108["杀鼠表"]
    )

    return test_mouse
