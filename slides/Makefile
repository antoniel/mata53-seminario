all:
		pdflatex slides.tex
		bibtex slides
		pdflatex slides.tex
		pdflatex slides.tex

c: clean

clean:
		rm slides.{aux,bbl,blg,log,nav,out,snm,toc,pdf}
