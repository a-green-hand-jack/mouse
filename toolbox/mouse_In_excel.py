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
        # 原来的工作表中的列名称
        self.add_food = "新增粮食"
        self.subtract_food = "剩余粮食"
        self.moues_weight_record = "体重记录"
        self.mouse_kill = "杀鼠表"

        # 新建立的工作表的名称
        self.add_food_week = "每周新增粮食"
        self.subtract_food_week = "每周剩余粮食"
        self.eat_food = "每周进食情况"

        # 计算体重变化和每周进食情况
        weight_change_df = self.Calculate_WD(self.excel_file[f"{self.moues_weight_record}"])
        self.sum_df = self.Calculate_WEH(self.excel_file[f"{self.add_food}"], add_food=self.add_food_week)
        self.sum_df_sub = self.Calculate_WEH(self.excel_file[f"{self.subtract_food}"], add_food=self.subtract_food_week)

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
        # 定义文件路径
        
        # 保存处理后的数据到相同的文件，覆盖原始文件
        with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for sheet_name, df in self.excel_file.items():
                df.to_excel(writer, sheet_name=sheet_name, index=True)

        return self.excel_file
    
    def make_excel_mouse(self, mouse_number, mouse_cage="unknown", mouse_food="MCD",mouse_description=None):
        # mouse = self.excel_file[f"{self.moues_weight_record}"].loc[f"{mouse_number}"]
        mouse = {}
        mouse_list = [f"{mouse_number}的体重",f"{mouse_number}的体重变化",f"{mouse_cage}的新增粮食",f"{mouse_number}的描述",f"{mouse_cage}的剩余粮食",f"{mouse_cage}的每周进食量"]
        mouse_weight = self.excel_file[f"{self.moues_weight_record}"][mouse_number]
        mouse_delta_weight = self.weight_change_df[mouse_number]

        mouse_location = self.file_path
        if mouse_cage != "unknown":
            mouse_date_food = self.sum_df[mouse_cage]
            mouse_date_food_sub = self.sum_df_sub[mouse_cage]
        if mouse_description :
            pass
        else:
            mouse_description = input(f"这里是小鼠{mouse_number}，位于{mouse_cage}，食物是{mouse_food},现在您正在从表格中初始化小鼠，请问您有什么额外的交代？")  

        mouse["name"] = mouse_number
        mouse["cage"] = mouse_cage
        mouse["杀鼠表"] = self.excel_file[self.mouse_kill]
        
        mouse[mouse_list[0]] = mouse_weight
        mouse[mouse_list[1]] = mouse_delta_weight
        mouse[mouse_list[2]] = mouse_date_food
        mouse[mouse_list[4]] = mouse_date_food_sub
        mouse[mouse_list[3]] = f"这里是小鼠{mouse_number}，位于{mouse_cage}，食物是{mouse_food}，数据保存在{self.file_path}\n"+ mouse_description
        mouse[mouse_list[5]] = mouse_date_food_sub.sub(mouse_date_food,fill_value=0)
        mouse["location"] = mouse_location
        return mouse

    def Calculate_WEH(self, weekly_eating_df, add_food="每周投喂食物数量"):
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
        self.excel_file[f"{add_food}"] = sum_df
        return sum_df

    def Calculate_WD(self, mouse_weigh, mouse_weight_change="每周老鼠体重变化"):
        """
        计算每周老鼠体重变化情况。

        Parameters:
            mouse_weigh (DataFrame): 包含老鼠体重记录的 DataFrame。
            mouse_weight_change (str, optional): 体重变化列的名称，默认为 "每周老鼠体重变化"。

        Returns:
            DataFrame: 包含每周老鼠体重变化情况的 DataFrame。
        """
        self.weight_change_df = mouse_weigh.diff()
        self.weight_change_df.iloc[0] = 0
        # self.weight_change = self.weight_change_df
        self.excel_file[f"{mouse_weight_change}"] = self.weight_change_df
        return self.weight_change_df

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


