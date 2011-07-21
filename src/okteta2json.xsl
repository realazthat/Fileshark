<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml">
 
  <xsl:output method="text"  encoding="UTF-8"/>
 
  <xsl:template match="/data">
    <xsl:apply-templates />
  </xsl:template>
 
  <xsl:template match="struct">
    {
      "name": "<xsl:value-of select="@name"/>",
      "type": "struct",
      "inner_types": [
	<xsl:apply-templates />
	]
    },
  </xsl:template>
  
  <xsl:template match="primitive">
    {
      "name": "<xsl:value-of select="@name"/>",
      "type": "<xsl:value-of select="@type"/>"
    },
  </xsl:template>
  
  <xsl:template match="bitfield">
    {
      "name": "<xsl:value-of select="@name"/>",
      "type": "<xsl:value-of select="@type"/>",
      "width": "<xsl:value-of select="@width"/>"
    },
  </xsl:template>
 
</xsl:stylesheet>
