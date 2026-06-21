USE [master]
GO
ALTER DATABASE [FUNewsManagement] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE [FUNewsManagement]
GO
CREATE DATABASE [FUNewsManagement]
GO
USE [FUNewsManagement]
GO

CREATE TABLE [dbo].[Category](
	[CategoryID] [smallint] IDENTITY(1,1) NOT NULL,
	[CategoryName] [nvarchar](100) NOT NULL,
	[CategoryDesciption] [nvarchar](250) NOT NULL,
	[ParentCategoryID] [smallint] NULL,
	[IsActive] [bit] NULL,
 CONSTRAINT [PK_Category] PRIMARY KEY CLUSTERED ([CategoryID] ASC)
)
GO

CREATE TABLE [dbo].[NewsArticle](
	[NewsArticleID] [nvarchar](20) NOT NULL,
	[NewsTitle] [nvarchar](400) NULL,
	[Headline] [nvarchar](150) NOT NULL,
	[CreatedDate] [datetime] NULL,
	[NewsContent] [nvarchar](4000) NULL,
	[NewsSource] [nvarchar](400) NULL,
	[CategoryID] [smallint] NULL,
	[NewsStatus] [bit] NULL,
	[CreatedByID] [smallint] NULL,
	[UpdatedByID] [smallint] NULL,
	[ModifiedDate] [datetime] NULL,
	[ImageUrl] [nvarchar](500) NULL,
	[ViewCount] [int] NULL DEFAULT 0,
 CONSTRAINT [PK_NewsArticle] PRIMARY KEY CLUSTERED ([NewsArticleID] ASC)
)
GO

CREATE TABLE [dbo].[Tag](
	[TagID] [int] IDENTITY(1,1) NOT NULL,
	[TagName] [nvarchar](50) NULL,
	[Note] [nvarchar](400) NULL,
 CONSTRAINT [PK_HashTag] PRIMARY KEY CLUSTERED ([TagID] ASC)
)
GO

CREATE TABLE [dbo].[NewsTag](
	[NewsArticleID] [nvarchar](20) NOT NULL,
	[TagID] [int] NOT NULL,
 CONSTRAINT [PK_NewsTag] PRIMARY KEY CLUSTERED ([NewsArticleID] ASC, [TagID] ASC)
)
GO

CREATE TABLE [dbo].[SystemAccount](
	[AccountID] [smallint] IDENTITY(1,1) NOT NULL,
	[AccountName] [nvarchar](100) NULL,
	[AccountEmail] [nvarchar](70) NULL,
	[AccountRole] [int] NULL,
	[AccountPassword] [nvarchar](70) NULL,
 CONSTRAINT [PK_SystemAccount] PRIMARY KEY CLUSTERED ([AccountID] ASC)
)
GO

SET IDENTITY_INSERT [dbo].[Category] ON 
GO
INSERT [dbo].[Category] ([CategoryID], [CategoryName], [CategoryDesciption], [ParentCategoryID], [IsActive]) VALUES (1, N'Academic news', N'This category can include articles about research findings...', 1, 1)
INSERT [dbo].[Category] ([CategoryID], [CategoryName], [CategoryDesciption], [ParentCategoryID], [IsActive]) VALUES (2, N'Student Affairs', N'This category can include articles about student activities...', 2, 1)
INSERT [dbo].[Category] ([CategoryID], [CategoryName], [CategoryDesciption], [ParentCategoryID], [IsActive]) VALUES (3, N'Campus Safety', N'This category can include articles about incidents...', 3, 1)
INSERT [dbo].[Category] ([CategoryID], [CategoryName], [CategoryDesciption], [ParentCategoryID], [IsActive]) VALUES (4, N'Alumni News', N'This category can include articles about the achievements...', 4, 1)
INSERT [dbo].[Category] ([CategoryID], [CategoryName], [CategoryDesciption], [ParentCategoryID], [IsActive]) VALUES (5, N'Capstone Project News', N'This category is typically a comprehensive report...', 5, 0)
GO
SET IDENTITY_INSERT [dbo].[Category] OFF
GO

INSERT [dbo].[NewsArticle] ([NewsArticleID], [NewsTitle], [Headline], [CreatedDate], [NewsContent], [NewsSource], [CategoryID], [NewsStatus], [CreatedByID], [UpdatedByID], [ModifiedDate], [ImageUrl], [ViewCount]) VALUES (N'1', N'University FU Celebrates Success of Alumni', N'University FU Celebrates Success of Alumni', CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'University FU recently commemorated the achievements of its esteemed alumni...', N'N/A', 4, 1, 1, 1, CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=1200&auto=format&fit=crop', 15)
INSERT [dbo].[NewsArticle] ([NewsArticleID], [NewsTitle], [Headline], [CreatedDate], [NewsContent], [NewsSource], [CategoryID], [NewsStatus], [CreatedByID], [UpdatedByID], [ModifiedDate], [ImageUrl], [ViewCount]) VALUES (N'2', N'Alumni Association Launches Mentorship Program', N'Mentorship Program for Recent Graduates', CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'The Alumni Association of University FU recently unveiled a new mentorship program...', N'Internet', 4, 1, 1, 1, CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1200&auto=format&fit=crop', 42)
INSERT [dbo].[NewsArticle] ([NewsArticleID], [NewsTitle], [Headline], [CreatedDate], [NewsContent], [NewsSource], [CategoryID], [NewsStatus], [CreatedByID], [UpdatedByID], [ModifiedDate], [ImageUrl], [ViewCount]) VALUES (N'3', N'Academic Department Announces Groundbreaking Initiatives', N'Groundbreaking Initiatives and Enhancements', CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'The Software Engineering Department at FU has unveiled a series of transformative initiatives...', N'N/A', 1, 1, 2, 2, CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1200&auto=format&fit=crop', 108)
INSERT [dbo].[NewsArticle] ([NewsArticleID], [NewsTitle], [Headline], [CreatedDate], [NewsContent], [NewsSource], [CategoryID], [NewsStatus], [CreatedByID], [UpdatedByID], [ModifiedDate], [ImageUrl], [ViewCount]) VALUES (N'4', N'Renowned Scholar Appointed as Head of AI', N'Scholar Appointed as Head of AI Department at FU', CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'FU proudly announces the appointment of David Nitzevet, a distinguished scholar in Machine Learning...', N'N/A', 1, 1, 2, 2, CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=1200&auto=format&fit=crop', 67)
INSERT [dbo].[NewsArticle] ([NewsArticleID], [NewsTitle], [Headline], [CreatedDate], [NewsContent], [NewsSource], [CategoryID], [NewsStatus], [CreatedByID], [UpdatedByID], [ModifiedDate], [ImageUrl], [ViewCount]) VALUES (N'5', N'New Research Findings Shed Light on STEM', N'New Research Findings Shed Light on STEM', CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'Groundbreaking research conducted by the Research Department of FU has unveiled significant findings...', N'N/A', 1, 1, 2, 2, CAST(N'2024-05-05T00:00:00.000' AS DateTime), N'https://images.unsplash.com/photo-1532094349884-543bc11b234d?q=80&w=1200&auto=format&fit=crop', 89)
GO

SET IDENTITY_INSERT [dbo].[Tag] ON 
GO
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (1, N'Education', N'Education Note')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (2, N'Technology', N'Technology Note')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (3, N'Research', N'Research Note')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (4, N'Innovation', N'Innovation Note')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (5, N'Campus Life', N'Campus Life Note')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (6, N'Faculty', N'Faculty Achievements')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (7, N'Alumni ', N'Alumni News')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (8, N'Events', N'University Events')
INSERT [dbo].[Tag] ([TagID], [TagName], [Note]) VALUES (9, N'Resources', N'Campus Resources')
GO
SET IDENTITY_INSERT [dbo].[Tag] OFF
GO

INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'1', 5)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'1', 7)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'1', 9)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'2', 5)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'2', 7)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'2', 8)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'2', 9)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'3', 1)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'3', 8)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'3', 9)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'4', 1)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'4', 4)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'4', 8)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'4', 9)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'5', 2)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'5', 3)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'5', 4)
INSERT [dbo].[NewsTag] ([NewsArticleID], [TagID]) VALUES (N'5', 6)
GO

SET IDENTITY_INSERT [dbo].[SystemAccount] ON 
GO
INSERT [dbo].[SystemAccount] ([AccountID], [AccountName], [AccountEmail], [AccountRole], [AccountPassword]) VALUES (1, N'Emma William', N'EmmaWilliam@FUNewsManagement.org', 2, N'@1')
INSERT [dbo].[SystemAccount] ([AccountID], [AccountName], [AccountEmail], [AccountRole], [AccountPassword]) VALUES (2, N'Olivia James', N'OliviaJames@FUNewsManagement.org', 2, N'@1')
INSERT [dbo].[SystemAccount] ([AccountID], [AccountName], [AccountEmail], [AccountRole], [AccountPassword]) VALUES (3, N'Isabella David', N'IsabellaDavid@FUNewsManagement.org', 1, N'@1')
INSERT [dbo].[SystemAccount] ([AccountID], [AccountName], [AccountEmail], [AccountRole], [AccountPassword]) VALUES (4, N'Michael Charlotte', N'MichaelCharlotte@FUNewsManagement.org', 1, N'@1')
INSERT [dbo].[SystemAccount] ([AccountID], [AccountName], [AccountEmail], [AccountRole], [AccountPassword]) VALUES (5, N'Steve Paris', N'SteveParis@FUNewsManagement.org', 1, N'@1')
GO
SET IDENTITY_INSERT [dbo].[SystemAccount] OFF
GO

ALTER TABLE [dbo].[Category]  WITH CHECK ADD  CONSTRAINT [FK_Category_Category] FOREIGN KEY([ParentCategoryID]) REFERENCES [dbo].[Category] ([CategoryID])
GO
ALTER TABLE [dbo].[NewsArticle]  WITH CHECK ADD  CONSTRAINT [FK_NewsArticle_Category] FOREIGN KEY([CategoryID]) REFERENCES [dbo].[Category] ([CategoryID]) ON UPDATE CASCADE ON DELETE CASCADE
GO
ALTER TABLE [dbo].[NewsArticle]  WITH CHECK ADD  CONSTRAINT [FK_NewsArticle_SystemAccount] FOREIGN KEY([CreatedByID]) REFERENCES [dbo].[SystemAccount] ([AccountID]) ON UPDATE CASCADE ON DELETE CASCADE
GO
ALTER TABLE [dbo].[NewsTag]  WITH CHECK ADD  CONSTRAINT [FK_NewsTag_NewsArticle] FOREIGN KEY([NewsArticleID]) REFERENCES [dbo].[NewsArticle] ([NewsArticleID])
GO
ALTER TABLE [dbo].[NewsTag]  WITH CHECK ADD  CONSTRAINT [FK_NewsTag_Tag] FOREIGN KEY([TagID]) REFERENCES [dbo].[Tag] ([TagID])
GO
