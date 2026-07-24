package=expat
$(package)_version=2.2.0
$(package)_download_path=https://toolchains.bootlin.com/downloads/releases/sources/expat-2.2.0
$(package)_file_name=expat-2.2.0.tar.bz2
$(package)_sha256_hash=d9e50ff2d19b3538bd2127902a89987474e1a4db8e43a66a4d1a712ab9a504ff

define $(package)_set_vars
$(package)_config_opts=--disable-static
endef

define $(package)_config_cmds
  $($(package)_autoconf)
endef

define $(package)_build_cmds
  $(MAKE)
endef

define $(package)_stage_cmds
  $(MAKE) DESTDIR=$($(package)_staging_dir) install
endef
