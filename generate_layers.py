import os

daos_dir = "PhanChiThong_DataAccess/DAOs"
repos_dir = "PhanChiThong_DataAccess/Repositories"
services_dir = "PhanChiThong_BusinessLogic/Services"

os.makedirs(daos_dir, exist_ok=True)
os.makedirs(repos_dir, exist_ok=True)
os.makedirs(services_dir, exist_ok=True)

models = ["SystemAccount", "Category", "NewsArticle", "Tag"]

# DAOs
for model in models:
    content = f"""using PhanChiThong_DataAccess.Models;
using System.Collections.Generic;
using System.Linq;
using Microsoft.EntityFrameworkCore;

namespace PhanChiThong_DataAccess.DAOs
{{
    public class {model}DAO
    {{
        private static {model}DAO instance = null;
        private static readonly object instanceLock = new object();
        private {model}DAO() {{ }}
        public static {model}DAO Instance
        {{
            get
            {{
                lock (instanceLock)
                {{
                    if (instance == null)
                    {{
                        instance = new {model}DAO();
                    }}
                    return instance;
                }}
            }}
        }}

        public List<{model}> GetAll()
        {{
            using var context = new FUNewsManagementContext();
            return context.{model}s.ToList();
        }}

        public {model} GetById(object id)
        {{
            using var context = new FUNewsManagementContext();
            return context.{model}s.Find(id);
        }}

        public void Add({model} entity)
        {{
            using var context = new FUNewsManagementContext();
            context.{model}s.Add(entity);
            context.SaveChanges();
        }}

        public void Update({model} entity)
        {{
            using var context = new FUNewsManagementContext();
            context.{model}s.Update(entity);
            context.SaveChanges();
        }}

        public void Delete({model} entity)
        {{
            using var context = new FUNewsManagementContext();
            context.{model}s.Remove(entity);
            context.SaveChanges();
        }}
    }}
}}
"""
    if model == "NewsArticle":
        content = content.replace(f"context.{model}s.ToList();", f"context.{model}s.Include(n => n.Category).Include(n => n.CreatedBy).Include(n => n.Tags).ToList();")
    if model == "Category":
        content = content.replace("context.Categorys", "context.Categories")
    
    with open(os.path.join(daos_dir, f"{model}DAO.cs"), "w") as f:
        f.write(content)

# Repositories
for model in models:
    interface_content = f"""using PhanChiThong_DataAccess.Models;
using System.Collections.Generic;

namespace PhanChiThong_DataAccess.Repositories
{{
    public interface I{model}Repository
    {{
        List<{model}> GetAll();
        {model} GetById(object id);
        void Add({model} entity);
        void Update({model} entity);
        void Delete({model} entity);
    }}
}}
"""
    with open(os.path.join(repos_dir, f"I{model}Repository.cs"), "w") as f:
        f.write(interface_content)

    impl_content = f"""using PhanChiThong_DataAccess.DAOs;
using PhanChiThong_DataAccess.Models;
using System.Collections.Generic;

namespace PhanChiThong_DataAccess.Repositories
{{
    public class {model}Repository : I{model}Repository
    {{
        public List<{model}> GetAll() => {model}DAO.Instance.GetAll();
        public {model} GetById(object id) => {model}DAO.Instance.GetById(id);
        public void Add({model} entity) => {model}DAO.Instance.Add(entity);
        public void Update({model} entity) => {model}DAO.Instance.Update(entity);
        public void Delete({model} entity) => {model}DAO.Instance.Delete(entity);
    }}
}}
"""
    with open(os.path.join(repos_dir, f"{model}Repository.cs"), "w") as f:
        f.write(impl_content)

# Services
for model in models:
    interface_content = f"""using PhanChiThong_DataAccess.Models;
using System.Collections.Generic;

namespace PhanChiThong_BusinessLogic.Services
{{
    public interface I{model}Service
    {{
        List<{model}> GetAll();
        {model} GetById(object id);
        void Add({model} entity);
        void Update({model} entity);
        void Delete({model} entity);
    }}
}}
"""
    with open(os.path.join(services_dir, f"I{model}Service.cs"), "w") as f:
        f.write(interface_content)

    impl_content = f"""using PhanChiThong_DataAccess.Models;
using PhanChiThong_DataAccess.Repositories;
using System.Collections.Generic;

namespace PhanChiThong_BusinessLogic.Services
{{
    public class {model}Service : I{model}Service
    {{
        private readonly I{model}Repository _repository;

        public {model}Service(I{model}Repository repository)
        {{
            _repository = repository;
        }}

        public List<{model}> GetAll() => _repository.GetAll();
        public {model} GetById(object id) => _repository.GetById(id);
        public void Add({model} entity) => _repository.Add(entity);
        public void Update({model} entity) => _repository.Update(entity);
        public void Delete({model} entity) => _repository.Delete(entity);
    }}
}}
"""
    with open(os.path.join(services_dir, f"{model}Service.cs"), "w") as f:
        f.write(impl_content)

print("Generated DAOs, Repositories, and Services successfully.")
