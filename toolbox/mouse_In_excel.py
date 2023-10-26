import pandas as pd

class DataProcessor:
    def __init__(self, file_path, output_file="output4.xlsx"):
        """
        初始化 DataProcessor 类。

        Parameters:
            file_path (str): Excel 文件路径。
            output_file (str, optional): 输出结果的 Excel 文件名，默认为 "output4.xlsx"。

        Attributes:
            file_path (str): Excel 文件路径。
            excel_file (dict): 存储不同工作表的数据的字典。

        Returns:
            None
        """
        self.file_path = file_path
        self.excel_file = self.get_mouse_data_from_excel()
        # 定义工作表中的列名称
        add_food = "粮食增减"
        add_food_sum_week = "每周粮食新增数量"
        subtract_food_week = "每周粮食剩余数量"
        eat_food = "每周进食情况"
        moues_weight_record = "体重记录"

        # 计算体重变化和每周进食情况
        weight_change_df = self.Calculate_WD(self.excel_file[f"{moues_weight_record}"])
        sum_df = self.Calculate_WEH(self.excel_file[f"{add_food}"], add_food=eat_food)

        # 保存结果到 Excel 文件
        self.Save2xlsx(f"{output_file}")

    def get_mouse_data_from_excel(self):
        """
        从 Excel 文件中获取数据，并存储到字典中。

        Returns:
            dict: 包含各个工作表数据的字典。
        """
        # 读取Excel文件，并处理数据
        xls = pd.ExcelFile(self.file_path)
        sheet_names = xls.sheet_names
        self.excel_file = {}
        for sheet_name in sheet_names:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            df.set_index(df.iloc[:, 0], inplace=True)
            df.drop(df.columns[[0]], axis=1, inplace=True)
            self.excel_file[sheet_name] = df
        return self.excel_file

    def Calculate_WEH(self, weekly_eating_df, add_food="每周投喂剩余食物数量的差值，也就是计算进食数量"):
        """
        计算每周进食情况。

        Parameters:
            weekly_eating_df (DataFrame): 包含每周进食情况的 DataFrame。
            add_food (str, optional): 进食情况列的名称，默认为 "每周投喂剩余食物数量的差值，也就是计算进食数量"。

        Returns:
            DataFrame: 包含每周进食情况的 DataFrame。
        """
        if not isinstance(weekly_eating_df.index, pd.DatetimeIndex):
            try:
                weekly_eating_df.index = pd.to_datetime(weekly_eating_df.index)
            except ValueError:
                weekly_eating_df.index = pd.to_datetime(weekly_eating_df.index, format='%Y-%m-%d')
        sum_df = weekly_eating_df.resample('7D').sum()
        self.sum_df = sum_df
        self.excel_file[f"{add_food}"] = sum_df
        return self.sum_df

    def Calculate_WD(self, mouse_weigh, mouse_weight_change="每周老鼠体重变化"):
        """
        计算每周老鼠体重变化情况。

        Parameters:
            mouse_weigh (DataFrame): 包含老鼠体重记录的 DataFrame。
            mouse_weight_change (str, optional): 体重变化列的名称，默认为 "每周老鼠体重变化"。

        Returns:
            DataFrame: 包含每周老鼠体重变化情况的 DataFrame。
        """
        weight_change_df = mouse_weigh.diff()
        weight_change_df.iloc[0] = 0
        self.weight_change = weight_change_df
        self.excel_file[f"{mouse_weight_change}"] = weight_change_df
        return weight_change_df

    def Save2xlsx(self, save_file="output.xlsx"):
        """
        保存处理后的数据到 Excel 文件。

        Parameters:
            save_file (str, optional): 保存的 Excel 文件名，默认为 "output.xlsx"。

        Returns:
            None
        """
        with pd.ExcelWriter(save_file) as writer:
            for sheet_name, sheet_df in self.excel_file.items():
                if isinstance(sheet_df.index, pd.DatetimeIndex):
                    sheet_df.index = pd.to_datetime(sheet_df.index).date
                sheet_df.to_excel(writer, sheet_name=sheet_name, index=True)



if __name__ == '__main__':

    # 获取用户输入的 Excel 文件路径
    input_data = input("请输入 Excel 文件路径：")

    # 获取用户输入的输出文件名
    output_file = input("请输入输出文件名：")

    # 创建 DataProcessor 对象，并传入用户输入的值
    data_processor = DataProcessor(input_data, output_file)


