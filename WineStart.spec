%global WSUser  WineStart
%global WSGroup WineStart

Name:           WineStart
Version:        1.0.0
Release:        1%{?dist}
Summary:        Run Wine applications under restricted session

License:        GPLv3+
Source0:        WineConsole.service
Source1:        WineStart@.service
Source2:        startx
Source3:        xinitrc

BuildArch:      noarch

BuildRequires:  systemd
Requires:       openbox
Requires:       /usr/bin/wine32
Requires:       /usr/bin/wine64
Requires(pre):  shadow-utils
%systemd_requires

%description
%{summary}.


%prep


%build


%install
rm -rf %{buildroot}
install -D -m644 -p %{SOURCE0} %{buildroot}%{_unitdir}/WineConsole.service
install -D -m644 -p %{SOURCE1} %{buildroot}%{_unitdir}/WineStart@.service
install -D -m755 -p %{SOURCE2} %{buildroot}%{_libexecdir}/WineStart/startx
install -D -m755 -p %{SOURCE3} %{buildroot}%{_libexecdir}/WineStart/xinitrc


%files
%{_unitdir}/WineConsole.service
%{_unitdir}/WineStart@.service
%{_libexecdir}/WineStart/startx
%{_libexecdir}/WineStart/xinitrc


%pre
getent group %{WSGroup} >/dev/null || groupadd -r %{WSGroup}
getent passwd %{WSUser} >/dev/null || \
    useradd -r -g %{WSGroup} -p '' -M -d /var/lib/%{WSUser} -s /bin/bash \
    -c "User for the Wine restricted session" %{WSUser}
cp -ar /etc/skel /var/lib/%{WSUser}
chmod 700 /var/lib/%{WSUser}
chown -R %{WSUser}:%{WSGroup} /var/lib/%{WSUser}
exit 0

%post
%systemd_post WineConsole.service

%preun
%systemd_preun WineConsole.service

%postun
%systemd_postun


%changelog
* Wed Feb 22 2017 Jajauma's Packages <jajauma@yandex.ru> - 1.0.0-1
- Initial release
