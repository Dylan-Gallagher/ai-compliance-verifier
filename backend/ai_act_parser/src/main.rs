use std::fs;
use scraper::{Html, Selector};
use regex::Regex;
use std::collections::HashMap;
use serde_json;
use std::fs::File;
use std::io::Write;
use serde::Serialize;

#[derive(Serialize)]
#[serde(untagged)]
enum Value {
    String(String),
    Map(HashMap<String, String>),
}

type FlexibleMap = HashMap<String, Value>;

fn main() {
    let ai_act = Html::parse_document(
        &fs::read_to_string("ai_act.html")
        .expect("Hardcoded path should not fail.")
    );

    let mut articles = HashMap::new();

    let div_selector = Selector::parse("div").unwrap();
    let point_re = Regex::new(r"\d{3}.\d{3}").unwrap();

    for point_div in ai_act.select(&div_selector) {
        // Article point divs have id="<article number>.<point number>" 
        //  e.g. id="012.002" is Article 12, Point 2
        let id = point_div.value().attr("id").unwrap_or("");
        if !point_re.is_match(id) {continue}
        let mut id_iter = id.split(".");

        let mut article: FlexibleMap = HashMap::new();

        // TODO: Do better error checking and return early after art 112
        // let art_num = match id_iter.next() {
        //     Some(num) => match num.parse() {
        //         Ok(val) => val,
        //         Err(_) => continue,
        //     }, 
        //     None => continue,
        // };
        //

        let art_num: i32 = id_iter.next().unwrap().parse().unwrap();
        let point_num: i32 = id_iter.next().unwrap().parse().unwrap();


        let mut child_elements = point_div.child_elements().peekable();
        let prefix = child_elements.next().unwrap().inner_html();

        let has_no_subpoints = child_elements.peek().is_none();
        if has_no_subpoints {
            // article.insert(format!("Point {point_num}"),Value::String(prefix.clone()));
            println!("Inserting art {art_num}, point {point_num}");
            articles.entry(format!("Article {art_num}")).or_insert_with(HashMap::new).insert(format!("Point {point_num}"), Value::String(prefix.clone()));
        }

        let mut subpoints = HashMap::new();
        for subpoint in child_elements {
            
            let subpoint = subpoint.child_elements().last();
            let mut subpoint = match subpoint {
                Some(e) => e.child_elements().next().unwrap().child_elements(),
                None => {
                    continue;
                }
            };

            let sub_point_index = subpoint
                                    .next() 
                                    .unwrap() // top <td>
                                    .child_elements() 
                                    .next() 
                                    .unwrap() 
                                    .inner_html();

            let sub_point_content = subpoint
                                    .next() 
                                    .unwrap() // bottom <td>
                                    .child_elements()
                                    .next()
                                    .unwrap()
                                    .inner_html();
            subpoints.insert(sub_point_index, sub_point_content);

            // println!("{prefix} {sub_point_index} {sub_point_content}");
        }

        if !has_no_subpoints{
            println!("Inserting art {art_num}, point {point_num}");
            articles.entry(format!("Article {art_num}")).or_insert_with(HashMap::new).insert(format!("Point {point_num}"), Value::Map(subpoints));
        }

        

        // if art_num > curr_art_num {
        //     println!("Inserting article {art_num} after point {point_num}");
        //     articles.insert(format!("Article {art_num}"), article);
        //     article = HashMap::new();
        //     curr_art_num = art_num;
        // }
    }

    let json = serde_json::to_string(&articles).unwrap();

    let mut file = File::create("result.json").unwrap();

    // Print the JSON string
    let _ = file.write_all(json.as_bytes());
}
