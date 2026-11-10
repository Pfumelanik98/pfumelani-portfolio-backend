from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from apps.core.views import ProfileView, SkillViewSet
from apps.projects.views import ProjectViewSet
from apps.education.views import EducationViewSet, CertificateViewSet, ResumeView
from apps.blog.views import BlogPostViewSet, BlogCategoryViewSet
from apps.contact.views import ContactMessageCreateView
from apps.integrations.views import GitHubRepositoriesView

router = DefaultRouter()
router.register("skills", SkillViewSet, basename="skill")
router.register("projects", ProjectViewSet, basename="project")
router.register("education", EducationViewSet, basename="education")
router.register("certificates", CertificateViewSet, basename="certificate")
router.register("blog/posts", BlogPostViewSet, basename="blog-post")
router.register("blog/categories", BlogCategoryViewSet, basename="blog-category")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/profile/", ProfileView.as_view(), name="profile"),
    path("api/v1/resume/", ResumeView.as_view(), name="resume"),
    path("api/v1/contact/", ContactMessageCreateView.as_view(), name="contact"),
    path("api/v1/github/repositories/", GitHubRepositoriesView.as_view(), name="github-repositories"),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/", include(router.urls)),
]
