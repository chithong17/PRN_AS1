USE [FUNewsManagement]
GO
UPDATE [dbo].[NewsArticle] 
SET NewsContent = N'University FU recently commemorated the achievements of its esteemed alumni in a grand ceremony. The event was attended by thousands of former students who have gone on to achieve remarkable success in their respective fields. The president of the university delivered an inspiring speech, highlighting the importance of lifelong learning and community engagement. Several alumni were awarded for their outstanding contributions to society, including breakthroughs in technology, healthcare, and public service. The ceremony concluded with a networking session where graduates shared their experiences and offered mentorship to current students.',
ImageUrl = N'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/FPT_University.jpg/1200px-FPT_University.jpg',
ViewCount = 650
WHERE NewsArticleID = N'1';

UPDATE [dbo].[NewsArticle] 
SET NewsContent = N'The Alumni Association of University FU recently unveiled a new mentorship program aimed at guiding recent graduates through their early career stages. This initiative pairs seasoned professionals with fresh talent to foster growth and knowledge transfer. The program offers one-on-one coaching, resume building workshops, and mock interviews. Early feedback has been overwhelmingly positive, with many mentees securing their dream jobs within months. The association plans to expand the program globally to reach all international alumni.',
ImageUrl = N'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Moraine_Lake_17092005.jpg/1200px-Moraine_Lake_17092005.jpg',
ViewCount = 420
WHERE NewsArticleID = N'2';

UPDATE [dbo].[NewsArticle] 
SET NewsContent = N'The Software Engineering Department at FU has unveiled a series of transformative initiatives designed to modernize the curriculum and equip students with cutting-edge skills. New courses in Artificial Intelligence, Cloud Computing, and Cybersecurity have been introduced. Additionally, the department has partnered with leading tech companies to provide students with hands-on internship opportunities. These enhancements are expected to significantly boost the employability of graduates and reinforce the university''s reputation as a premier institution for technical education.',
ImageUrl = N'https://images.pexels.com/photos/1181675/pexels-photo-1181675.jpeg?auto=compress&cs=tinysrgb&w=1200',
ViewCount = 890
WHERE NewsArticleID = N'3';

UPDATE [dbo].[NewsArticle] 
SET NewsContent = N'FU proudly announces the appointment of David Nitzevet, a distinguished scholar in Machine Learning, as the new Head of the AI Department. Professor Nitzevet brings over two decades of research experience and has published extensively in top-tier journals. His vision for the department includes fostering interdisciplinary research, expanding laboratory facilities, and launching a new master''s program in Data Science. Students and faculty alike are thrilled to welcome such a visionary leader to the academic community.',
ImageUrl = N'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=1200',
ViewCount = 550
WHERE NewsArticleID = N'4';

UPDATE [dbo].[NewsArticle] 
SET NewsContent = N'Groundbreaking research conducted by the Research Department of FU has unveiled significant findings that could revolutionize renewable energy technologies. The team discovered a novel material capable of storing solar energy with unprecedented efficiency. This breakthrough has the potential to drastically reduce the cost of solar panels and accelerate the global transition to clean energy. The university has filed several patents and is currently in talks with industry partners for commercialization.',
ImageUrl = N'https://images.pexels.com/photos/159358/construction-site-build-construction-work-159358.jpeg?auto=compress&cs=tinysrgb&w=1200',
ViewCount = 780
WHERE NewsArticleID = N'5';
GO
