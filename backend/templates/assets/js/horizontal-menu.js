"use strict";
$(document).ready(function() {
	$.fn.nav = function () {
		return this.each( function() {
			var getNav		= $(this),
				top 		= getNav.data('top') || getNav.offset().top,
				mdTop 		= getNav.data('md-top') || getNav.offset().top,
				xlTop 		= getNav.data('xl-top') || getNav.offset().top,
				navigation 	= getNav.find('.horizontal-menu'),
				getWindow 	= $(window).outerWidth(),
				anim 		= getNav.data('animate-prefix') || '',
				getIn 		= navigation.data('in'),
				getOut 		= navigation.data('out');
				$(window).on('resize', function(){
					getWindow 	= $(window).outerWidth();
				});
				getNav.find('.horizontal-menu').each(function(){
				var $menu = $(this);
				$menu.on('click', function(e) {
					if ( 'A' == e.target.tagName ) {
						$menu.find('li.active').removeClass('active');
						$(e.target).parent().addClass('active');
					}
				});
				$menu.find('li.active').removeClass('active');
				$menu.find( 'a[href="'+ location.href +'"]' ).parent('li').addClass('active');
			});
			/* -- Mobile Navbar -- */
			if( getNav.hasClass('mobile-navbar') ) {
				var $collapse = getNav.find('.navbar-collapse');
				if ( getNav.hasClass('navbar-reverse') ) {
					$collapse.on('shown.bs.collapse', function() {
						$('body').addClass('mobile-right');
					});
					$collapse.on('hide.bs.collapse', function() {
						$('body').removeClass('mobile-right');
					});
				}
				else {
					$collapse.on('shown.bs.collapse', function() {
						$('body').addClass('mobile-left');
					});
					$collapse.on('hide.bs.collapse', function() {
						$('body').removeClass('mobile-left');
					});
				}
			}
			/* -- Fixed Navbar -- */
			function stickyNav() {
				var scrollTop = $(window).scrollTop(),
					winWidth  = $(window).outerWidth();
				if( winWidth > 1599 && scrollTop > xlTop ) {
					getNav.addClass('sticky-navbar');
				}
				else if( winWidth > 1199 && scrollTop > top ) {
					getNav.addClass('sticky-navbar');
				}
				else if( winWidth > 991 && scrollTop > mdTop ) {
					getNav.addClass('sticky-navbar');
				}
				else {
					getNav.removeClass('sticky-navbar');
				}
			}
			if( getNav.hasClass('fixed-navbar') ) {
				$(window).on('scroll', function() {
					stickyNav();
				});
				$(window).on('resize', function() {
					stickyNav();
				});
				if ( getWindow > 991 && $(window).scrollTop() > top ) {
					getNav.addClass('sticky-navbar');
				}
			}
			/* -- Events -- */
			getNav.find('.horizontal-menu, .extension-nav').each(function(){
				var menu = this;
				$('.dropdown-toggle', menu).on('click', function (e) {
					e.stopPropagation();
					return false;
				});
				$('.dropdown-menu', menu).addClass(anim+'animated');
				$('.dropdown', menu).on('mouseenter', function(){
					var dropdown = this;
					$('.dropdown-menu', dropdown).eq(0).removeClass(getOut).stop().fadeIn().addClass(getIn);
					$(dropdown).addClass('on');
				});
				$('.dropdown', menu).on('mouseleave', function(){
					var dropdown = this;
					$('.dropdown-menu', dropdown).eq(0).removeClass(getIn).stop().fadeOut().addClass(getOut);
					$(dropdown).removeClass('on');
				});
				$('.mega-menu-col', menu).children('.sub-menu').removeClass('dropdown-menu '+anim+'animated');
			});
			if( getWindow < 992 ) {
				/* -- Mega Menu -- */
				getNav.find('.menu-item-has-mega-menu').each(function(){
					var megamenu 	= this,
						$columnMenus = [];
					$('.mega-menu-col', megamenu).children('.sub-menu').addClass('dropdown-menu '+anim+'animated');
					$('.mega-menu-col', megamenu).each(function(){
						var megamenuColumn = this;
						$('.mega-menu-col-title', megamenuColumn).on('mouseenter', function(){
							var title = this;
							$(title).closest('.mega-menu-col').addClass('on');
							$(title).siblings('.sub-menu').stop().fadeIn().addClass(getIn);
						});
						if( !$(megamenuColumn).children().is('.mega-menu-col-title') ) {
							$columnMenus.push( $(megamenuColumn).children('.sub-menu') );
						}
					});
					$(megamenu).on('mouseenter', function(){
						var submenu;
						for (submenu in $columnMenus) {
							$columnMenus[ submenu ].stop().fadeIn().addClass(getIn);
						}	
					});
					$(megamenu).on('mouseleave', function() {
						$('.dropdown-menu', megamenu).stop().fadeOut().removeClass(getIn);
						$('.mega-menu-col', megamenu).removeClass('on');
					});
				});
			}
		});
	}
	$('.horizontal-nav').nav();
});