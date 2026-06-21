import os
import re

def generate():
    base_file = "FUNewsManagement.sql"
    update_file = "FUNewsManagement_v2_update.sql"
    insert_more_file = "FUNewsManagement_v2_insert_more.sql"
    final_file = "FUNewsManagement_Final.sql"

    with open(base_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add new columns to NewsArticle
    target = "[ModifiedDate] [datetime] NULL,\n CONSTRAINT [PK_NewsArticle] PRIMARY KEY CLUSTERED"
    replacement = "[ModifiedDate] [datetime] NULL,\n\t[ImageUrl] [nvarchar](500) NULL,\n\t[ViewCount] [int] NULL,\n CONSTRAINT [PK_NewsArticle] PRIMARY KEY CLUSTERED"
    if target in content:
        content = content.replace(target, replacement)
    else:
        target = "[ModifiedDate] [datetime] NULL,\n CONSTRAINT [PK_NewsArticle] PRIMARY KEY CLUSTERED"
        content = content.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))

    content = content.replace("[FUNewsManagementFall2024]", "[FUNewsManagement]")

    # Inject DROP DATABASE if exists logic
    drop_script = """
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'FUNewsManagement')
BEGIN
    ALTER DATABASE [FUNewsManagement] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE [FUNewsManagement];
END
GO
"""
    if "USE [master]\nGO\n" in content:
        content = content.replace("USE [master]\nGO\n", "USE [master]\nGO\n" + drop_script, 1)
    else:
        content = content.replace("USE [master]\r\nGO\r\n", "USE [master]\r\nGO\r\n" + drop_script, 1)

    last_use_master_idx = content.rfind("USE [master]")
    
    with open(update_file, 'r', encoding='utf-8') as f:
        update_content = f.read()
        
    # We only want to update ImageUrl and ViewCount, NOT NewsContent!
    # Let's use regex to remove 'NewsContent = N'...',' from update_content
    # The text is: SET NewsContent = N'....', \n ImageUrl = N'...'
    update_content = re.sub(r"NewsContent\s*=\s*N'.*?',\s*", "", update_content, flags=re.DOTALL)
    
    # Remove the USE [FUNewsManagement]
    update_content = update_content.replace("USE [FUNewsManagement]\nGO\n", "")
    update_content = update_content.replace("USE [FUNewsManagement]\r\nGO\r\n", "")
    
    with open(insert_more_file, 'r', encoding='utf-8') as f:
        insert_content = f.read()

    insert_content = insert_content.replace("USE [FUNewsManagement]\nGO\n", "")
    insert_content = insert_content.replace("USE [FUNewsManagement]\r\nGO\r\n", "")

    combined_extras = "\n-- ======= UPDATES & NEW DATA =======\n" + update_content + "\n" + insert_content + "\n"

    if last_use_master_idx != -1 and last_use_master_idx > len(content) - 1000:
        final_content = content[:last_use_master_idx] + combined_extras + content[last_use_master_idx:]
    else:
        final_content = content + combined_extras

    with open(final_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print("Successfully generated FUNewsManagement_Final.sql")

if __name__ == '__main__':
    generate()
