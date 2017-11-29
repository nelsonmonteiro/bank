from django.contrib.staticfiles.storage import CachedFilesMixin
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
from filebrowser.storage import S3BotoStorageMixin
from pipeline.storage import PipelineMixin
import urllib


class CustomCachedFilesMixin(CachedFilesMixin):
    def url(self, *a, **kw):
        s = super(CustomCachedFilesMixin, self).url(*a, **kw)
        if isinstance(s, str):
            s = s.encode('utf-8', 'ignore')
        scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(s)
        path = urllib.parse.quote(path, '/%')
        qs = urllib.parse.quote_plus(qs, ':&=')
        return urllib.parse.urlunsplit((str(scheme), str(netloc), str(path), str(qs), str(anchor)))


class S3BotoStorageSafe(PipelineMixin, CustomCachedFilesMixin, S3BotoStorage, S3BotoStorageMixin):
    pass


StaticFilesStorage = lambda: S3BotoStorageSafe(
    bucket=settings.STATIC_FILES_BUCKET, custom_domain=settings.STATIC_FILES_DOMAIN)
DefaultFilesStorage = lambda: S3BotoStorageSafe(
    bucket=settings.DEFAULT_FILES_BUCKET, custom_domain=settings.DEFAULT_FILES_DOMAIN)

