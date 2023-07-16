# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os
import re

import pandas as pd
from openpyxl.utils.exceptions import IllegalCharacterError


class BilibiliScrapyPipeline:
    groupby = ''

    def open_spider(self, spider):
        self.file = open("video_info.txt", 'w', encoding="utf-8")

        # Define the custom directory path
        dir = "../../data/"

        # Create the directory if it doesn't exist
        if not os.path.exists(dir):
            os.makedirs(dir)

        # rank list excel table
        self.rank_writer = pd.ExcelWriter(os.path.join(dir, 'rank_list.xlsx'), engine='openpyxl')
        self.rank_sheet_names = set()

        # weekly list excel table
        self.weekly_writer = pd.ExcelWriter(os.path.join(dir, 'weekly_list.xlsx'), engine='openpyxl')
        self.weekly_sheet_names = set()

        # Initialize item list
        self.rank_items = []
        self.weekly_items = []

    def close_spider(self, spider):
        self.file.close()

        # Convert item list to DataFrame
        rank_df = pd.DataFrame(self.rank_items)
        weekly_df = pd.DataFrame(self.weekly_items)

        # Group items by category and weekly_name
        rank_grouped = rank_df.groupby('category')
        weekly_grouped = weekly_df.groupby('weekly_name')

        # write
        try:
            for group, group_df in rank_grouped:
                group_df.to_excel(self.rank_writer, index=False, sheet_name=str(group))

            for group, group_df in weekly_grouped:
                group_df.to_excel(self.weekly_writer, index=False, sheet_name=str(group))
        except IllegalCharacterError as e:
            # 遇到非法字符时，直接跳过该记录
            print(f"Illegal character found. Skipping the record.")
            pass

        # save rank list excel file
        self.rank_writer._save()
        # save weekly list excel file
        self.weekly_writer._save()

    def process_item(self, item, spider):
        # file type
        item_list = None
        pre_dir = ""
        if item['category'] != -1:
            pre_dir = f"../../data/rank_list/{item['category']}"
            item_list = self.rank_items
        if item['weekly_id'] != -1:
            pre_dir = f"../../data/weekly_list/{item['weekly_name']}"
            item_list = self.weekly_items

        # Append item to the list
        item_dict = dict(item)
        item_dict.pop('bulletScreen')
        item_list.append(item_dict)

        # Create the directory if it doesn't exist
        if not os.path.exists(pre_dir):
            os.makedirs(pre_dir)

        # gen filename
        single_video_filename = f"{item['rank']}_{item['title']}_{item['author']}.txt"

        # replace: some title has '/', '\', '|' etc., which are not available in filename
        special_chars = r'(con|prn|aux|nul|(com|lpt)[1-9])(\..*)?$|[\\/:*?"<>|]+'
        single_video_filename = re.sub(special_chars, '_', single_video_filename)
        # gen file dir
        single_video_filedir = f"{pre_dir}/{single_video_filename}"

        # write
        with open(file=single_video_filedir, mode="w", encoding="utf-8") as f:
            f.write(str(item))

        # return
        return item
