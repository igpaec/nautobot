import Card from "react-bootstrap/Card"
import CardHeader from "react-bootstrap/CardHeader"
import Link from "next/link"
import { nautobot_url } from "pages"
import Tab from "react-bootstrap/Tab"
import Table from "react-bootstrap/Table"
import Tabs from "react-bootstrap/Tabs"
import Layout from "components/layout"
import { useRouter } from "next/router"
import useSWR from "swr"

const fetcher = (url) => fetch(url, { credentials: "include" }).then((res) => res.json())
const fetcherHTML = (url) => fetch(url, { credentials: "include" }).then((res) => res.text())
const fetcherTabs = (url) => fetch(url, { credentials: "include" }).then((res) => {

  return res.json().then((data) => {
    console.log(data)

    let tabs = []
    data.tabs.map((tab_top) => {
      Object.keys(tab_top).map((tab_key) => {
        let tab = tab_top[tab_key]
        console.log(tab)
        tabs.push(<Tab title={tab.title} eventKey={tab.title}><div dangerouslySetInnerHTML={{__html: "<p>I can be retrieved from "+tab.url+"</p>"}} /></Tab>)
      })
    })
    console.log(tabs)
    return tabs
  })
})

export default function SitesObjectRetrieve() {

  var pluginConfig = []
  const router = useRouter()
  const { id } = router.query
  const { data: objectData, error } = useSWR(() => nautobot_url + "/api/dcim/sites/" + id + "/", fetcher)
  const { data: pluginHTML, _ } = useSWR(() => nautobot_url + "/dcim/sites/" + objectData.slug + "/?fragment=true", fetcherHTML)
  var { data: pluginConfig, _2 } = useSWR(() => nautobot_url + "/dcim/sites/" + objectData.slug + "/?format=json", fetcherTabs)
  if (error) return <div>Failed to load site</div>
  if (!objectData) return <></>
  return (
    <Layout>
      <h1>{objectData.name}</h1>
      <p>
        <small className="text-muted">
          {objectData.created &&
            <>Created {objectData.created} &middot; </>
          }
          <> Updated <span title={objectData.last_updated}>xyz seconds</span> ago</>
        </small>
      </p>
      <div className="pull-right noprint"></div>
      <Tabs defaultActiveKey="site">
        <Tab eventKey="site" title="Site">
          <Card>
            <CardHeader>
              <strong>Site</strong>
            </CardHeader>
            <Table hover>
              <tbody>
                <tr>
                  <td>Status</td>
                  <td>
                    <span className="label">
                      {objectData.status ? <>{objectData.status.label}</> : "—"}
                    </span>
                  </td>
                </tr>
                <tr>
                  <td>Region</td>
                  <td>
                    {objectData.region ?
                      <Link href={objectData.region.url}>{objectData.region.display}</Link> : "—"}
                  </td>
                </tr>
                <tr>
                  <td>Tenant</td>
                  <td>
                    {objectData.tenant ?
                      <Link href={objectData.tenant.url}>{objectData.tenant.display}</Link> : "—"}
                  </td>
                </tr>
                <tr>
                  <td>Facility</td>
                  <td>
                    {objectData.facility ? <>{objectData.facility}</> : "—"}
                  </td>
                </tr>
                <tr>
                  <td>AS Number</td>
                  <td>
                    {objectData.asn ? <>{objectData.asn}</> : "—"}
                  </td>
                </tr>
                <tr>
                  <td>Time Zone</td>
                  <td>
                    {objectData.time_zone ? <>{objectData.time_zone}</> : "—"}
                  </td>
                </tr>
                <tr>
                  <td>Description</td>
                  <td>
                    {objectData.description ? <>{objectData.description}</> : "—"}
                  </td>
                </tr>
              </tbody>
            </Table>
          </Card>

          <br />
          <div dangerouslySetInnerHTML={{__html: pluginHTML}} />
          <br />
        </Tab>
        <Tab eventKey="advanced" title="Advanced">
          <img src="https://raw.githubusercontent.com/nautobot/nautobot/develop/nautobot/docs/nautobot_logo.svg"></img>
        </Tab>
        <Tab eventKey="notes" title="Notes" />
        <Tab eventKey="change_log" title="Change Log">
          <div dangerouslySetInnerHTML={{__html: "<p>Your html code here.<p>"}} />
        </Tab>
        {pluginConfig}
      </Tabs>
    </Layout>
  )
}
