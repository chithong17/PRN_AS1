using PhanChiThong_DataAccess.Models;
using System.Collections.Generic;
using System.Linq;
using Microsoft.EntityFrameworkCore;

namespace PhanChiThong_DataAccess.DAOs
{
    public class NewsArticleDAO
    {
        private static NewsArticleDAO instance = null;
        private static readonly object instanceLock = new object();
        private NewsArticleDAO() { }
        public static NewsArticleDAO Instance
        {
            get
            {
                lock (instanceLock)
                {
                    if (instance == null)
                    {
                        instance = new NewsArticleDAO();
                    }
                    return instance;
                }
            }
        }

        public List<NewsArticle> GetAll()
        {
            using var context = new FUNewsManagementContext();
            return context.NewsArticles.Include(n => n.Category).Include(n => n.CreatedBy).Include(n => n.Tags).ToList();
        }

        public NewsArticle GetById(object id)
        {
            using var context = new FUNewsManagementContext();
            return context.NewsArticles.Find(id);
        }

        public void Add(NewsArticle entity)
        {
            using var context = new FUNewsManagementContext();
            context.NewsArticles.Add(entity);
            context.SaveChanges();
        }

        public void Update(NewsArticle entity)
        {
            using var context = new FUNewsManagementContext();
            context.NewsArticles.Update(entity);
            context.SaveChanges();
        }

        public void Delete(NewsArticle entity)
        {
            using var context = new FUNewsManagementContext();
            var trackedEntity = context.NewsArticles.Include(n => n.Tags).FirstOrDefault(n => n.NewsArticleId == entity.NewsArticleId);
            if (trackedEntity != null)
            {
                trackedEntity.Tags.Clear();
                context.SaveChanges();

                context.NewsArticles.Remove(trackedEntity);
                context.SaveChanges();
            }
        }
    }
}
