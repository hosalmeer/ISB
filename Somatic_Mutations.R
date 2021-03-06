#' # Somatic Mutations
#' 
#' The goal of this notebook is to introduce you to the Somatic Mutations BigQuery table.
#' This table is based on the open-access somatic mutation calls available in MAF files at the DCC. In addition to uploading all current MAF files from the DCC, the mutations were also annotated using Oncotator. A subset of the columns in the underlying MAF files and a subset of the Oncotator outputs were then assembled in this table.
#' In addition, the ETL process includes several data-cleaning steps because many tumor types actually have multiple current MAF files and therefore potentially duplicate mutation calls. In some cases, a tumor sample may have had mutations called relative to both a blood-normal and an adjacent-tissue sample, and in other cases MAF files may contain mutations called on more than one aliquot from the same sample. Every effort was made to include all of the available data at the DCC while avoiding having multiple rows in the mutation table describing the same somatic mutation. Note, however, that if the same mutation was called by multiple centers and appeared in different MAF files, it may be described on muliple rows (as you will see later in this notebook). Furthermore, in some cases, the underlying MAF file may have been based on a multi-center mutationa-calling exercise, in which case you may see a list of centers in the Center field, eg "bcgsc.ca;broad.mit.edu;hgsc.bcm.edu;mdanderson.org;ucsc.edu".
#' In conclusion, if you are counting up the number of mutations observed in a sample or a patient or a tumor-type, be sure to include the necessary GROUP BY clause(s) in order to avoid double-counting!
#' 
#' As usual, in order to work with BigQuery, you need to import the bigquery module (gcp.bigquery) and you need to know the name(s) of the table(s) you are going to be working with:
#' 
## ----message=FALSE-------------------------------------------------------
require(bigrquery) || install.packages("bigrquery")
require(ggplot2) || install.packages("ggplot2")

project = "exemplary-point-148206"

library(ISBCGCExamples)

mutTable <- "[isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]"

#' 
#' Let's start by taking a look at the table schema:
#' 
## ------------------------------------------------------------------------
querySql <- paste("SELECT * FROM ",mutTable," limit 10000", sep="")
result <- query_exec(querySql, project=project)
data.frame(Columns=colnames(result))



#' 
#' That's a lot of fields! Let's dig in a bit further to see what is included in this table. For example let's count up the number of unique patients, tumor-samples, and normal-samples based on barcode identifiers:
#' 
#' 
## ------------------------------------------------------------------------
# for (x in c("ParticipantBarcode", "Tumor_SampleBarcode", "Normal_SampleBarcode")) {
#   querySql <- paste("SELECT COUNT(DISTINCT(",x,"), 25000) AS n ",
#                     "FROM ",mutTable)
#   result <- query_exec(querySql, project=project)
#   cat(x, ": ", result[[1]], "\n")
# }

#' 
#' Now let's look at a few key fields and find the top-5 most frequent values in each field:
#' 
## ------------------------------------------------------------------------
# 
# buildQuery <- function(x) {
#   paste("
#   SELECT ",x,", COUNT(*) AS n
#   FROM [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
#   WHERE ( ",x," IS NOT NULL )
#   GROUP BY ",x,"
#   ORDER BY n DESC
#   LIMIT 500", sep="")
# }
# 
# query_exec(buildQuery("Hugo_Symbol"), project=project)
# query_exec(buildQuery("Center"), project=project)
# query_exec(buildQuery("Mutation_Status"), project=project)
# query_exec(buildQuery("Protein_Change"), project=project)
# 
#' 
#' Everyone probably recognizes the V600E mutation in the previous result, so let's use that well-known BRAF mutation as a way to explore what other information is available in this table.
#' 
## ------------------------------------------------------------------------
 # 
 # querySql <- "
 # SELECT
 #   Tumor_SampleBarcode,
 #   Study,
 #   Hugo_Symbol,
 #   Genome_Change,
 #   Protein_Change
 # FROM
 #   [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
 # WHERE
 #   ( Hugo_Symbol='BRAF'
 #     AND Protein_Change='p.V600E' )
 # GROUP BY
 #   Tumor_SampleBarcode,
 #   Study,
 #   Hugo_Symbol,
 #   Genome_Change,
 #   Protein_Change
 # ORDER BY
 #   Study,
 #   Tumor_SampleBarcode"
 # 
 # result <- query_exec(querySql, project=project)
 # head(result)
 # 
# #' 
# #' Let's count these mutations up by study (tumor-type):
# #' 
# ## ------------------------------------------------------------------------
# 
# querySql <- "
# SELECT
#   Study, COUNT(*) AS n
# FROM
#   [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
# WHERE
#   ( Hugo_Symbol='BRAF'
#     AND Protein_Change='p.V600E' )
# GROUP BY
#   Study
# HAVING n > 1
# ORDER BY n DESC
# "
# 
# query_exec(querySql, project=project)
# 
# #' 
# #' You may have noticed that in our earlier query, we did a GROUP BY to make sure that we didn't count the same mutation called on the same sample more than once. We might want to GROUP BY patient instead to see if that changes our counts -- we may have multiple samples from some patients.
# #' 
# ## ------------------------------------------------------------------------
# 
# querySql <- "
# SELECT
#   ParticipantBarcode,
#   Study,
#   Hugo_Symbol,
#   Genome_Change,
#   Protein_Change
# FROM
#   [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
# WHERE
#   ( Hugo_Symbol='BRAF'
#     AND Protein_Change='p.V600E' )
# GROUP BY
#   ParticipantBarcode,
#   Study,
#   Hugo_Symbol,
#   Genome_Change,
#   Protein_Change
# ORDER BY
#   Study,
#   ParticipantBarcode"
# 
# result <- query_exec(querySql, project=project)
# head(result)
# table(result$Study)
# 
# 
# #' 
# #' When we counted the number of mutated samples, we found 261 THCA samples, but when we counted the number of patients, we found 258 THCA patients, so let's see what's going on there.
# #' 
# #' 
# ## ------------------------------------------------------------------------
# querySql <- "
# SELECT
#   ParticipantBarcode,
#   COUNT(*) AS m
# FROM (
#   SELECT
#     ParticipantBarcode,
#     Tumor_SampleBarcode,
#     COUNT(*) AS n
#   FROM
#     [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
#   WHERE
#     ( Hugo_Symbol='BRAF'
#       AND Protein_Change='p.V600E'
#       AND Study='THCA' )
#   GROUP BY
#     ParticipantBarcode,
#     Tumor_SampleBarcode,
#     )
# GROUP BY
#   ParticipantBarcode
# HAVING
#   m > 1
# ORDER BY
#   m DESC"
# 
# result <- query_exec(querySql, project=project)
# head(result)
# 
# #' 
# #' Sure enough, we see that the same mutation is reported twice for each of these three patients. Let's look at why:
# #' 
# ## ------------------------------------------------------------------------
# querySql <- "
# SELECT
#   ParticipantBarcode,
#   Tumor_SampleBarcode,
#   Tumor_SampleTypeLetterCode,
#   Normal_SampleBarcode,
#   Normal_SampleTypeLetterCode,
#   Center,
# FROM
#   [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
# WHERE
#   ( Hugo_Symbol='BRAF'
#     AND Protein_Change='p.V600E'
#     AND Study='THCA'
#     AND ParticipantBarcode='TCGA-EM-A2P1' )
# ORDER BY
#   Tumor_SampleBarcode,
#   Normal_SampleBarcode,
#   Center"
# 
# result <- query_exec(querySql, project=project)
# head(result)
# 
#' 
#' Aha! not only did this patient provide both a primary tumor (TP) and a metastatic (TM) sample, but we have mutation calls from three different centers.
#' 
#' Finally, let's pick out one of these mutations and see what some of the other fields in this table can tell us:
#' 
## ------------------------------------------------------------------------
# 
q0Sql <- "
SELECT
  ParticipantBarcode,
  Tumor_SampleTypeLetterCode,
  Normal_SampleTypeLetterCode,
  Study,
  Center,
  Variant_Type,
  Variant_Classification,
  Genome_Change,
  cDNA_Change,
  Protein_Change,
  UniProt_Region,
  COSMIC_Total_Alterations_In_Gene,
  DrugBank,
  Hugo_Symbol
FROM
  [isb-cgc:tcga_201510_alpha.Somatic_Mutation_calls]
WHERE
  ( 
    Study='BRCA'
    )
"


# q0Sql <- "
# SELECT * FROM INFORMATION_SCHEMA.TABLES
# "

result <- query_exec(q0Sql, project=project)
head(result)
