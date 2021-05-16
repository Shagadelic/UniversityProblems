### R script for MA plots

## x: Data.frame with samples in columns
## log: TRUE, if data need to be log-transformed
#       FALSE, if data are already log-transformed
# labels: names of the sample (default: column names of x)
# file: path for pdf file (e.g. "graphics/MAplot.pdf")
# ...: additional arguments to affy::ma.plot

# (... in general means that you can enter arguments not explicitly mentioned
# in the function definition. They will be forwarded two the function ma.plot
# which is used inside the function. This is handy, if you want to control all
# arguments of a function but do not want to explicitly write them down when
# defining the outer function)

MAPlots <- function(X, log = FALSE,  labels = colnames(X), file, ...) {
  require(affy) # load affy package

  # function to plot a singe MA Plot (comparing 2 samples with each other)
  MAPlot_single <- function(x1, x2, log = FALSE, ...) {
    # log transform data if necessary
    if(log) {
      x1 <- log2(x1)
      x2 <- log2(x2)
    }
    # calculate M and A values:
    M <- na.omit(x1 - x2)
    A <- na.omit((x1 + x2)/2)
    # plot the MA-plot using ma.plot:
    ma.plot(A = A, M = M, pch = 16, cex = 0.7, show.statistics = FALSE, ...)
  }

  pdf(file) # start pdf device
  # use two nested for loops to plot MA-Plots for alle combinations
  # of sample pairs
  for(i in 1:(ncol(X)-1)) {
    for (j in (i + 1):ncol(X)) {
        main = paste(labels[i], labels[j]) # define plot title
      MAPlot_single(X[,i], X[, j], log = log, main = main, ...)
    }
  }
  dev.off() # close device
}


